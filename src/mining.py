import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from githubutils import GitHub


bothSentimentsMerged = {
    'posNeg': 0,
    'posNeu': 0,
    'negNeu': 0,
    'sameEvenAfterAverage': 0,
    'allThreeSameEvenAfterAverage': 0,
    'sameEvenAfterAverageForAuthor': 0,
    'posNegBothOccurredForAuthor': 0
}

bothSentimentsNotMerged = {
    'posNeg': 0,
    'posNeu': 0,
    'negNeu': 0,
    'sameEvenAfterAverage': 0
}

def main():
    gh = GitHub('GitID', 'AccessKey')
    projectList = {
        'statsmodels': 'statsmodels',
        'webpack': 'webpack',
        'thirtybees': 'thirtybees',
        'Miserlou': 'Zappa'
    }

    for i, j in projectList.iteritems():
        print "Collecting for {0}/{1}".format(i, j)

        f = open('{0}_{1}.csv'.format(i, j), 'wt')
        writer = csv.writer(f)
        writer.writerow(('sha', 'authorM', 'comments', 'merged'))

        pulls = gh.doApiCall('repos/{0}/{1}/pulls/'.format(i, j),
                             params={'state': 'all', 'sort': 'popularity', 'direction': 'desc'})

        for pull in pulls:
            pullsWithComments = {}
            pullSha = pull['merge_commit_sha']
            authorName = pull['user']['login']
            pullsWithComments[pullSha] = {'authorComments': [pull['body']], 'otherComments': []}

            commentsList = gh.doApiCall('repos/{0}/{1}/issues/{2}/comments'.format(i, j, pull['number']))

            for comment in commentsList:
                if comment['user']['login'] == authorName:
                    message = cleanMessage(comment['body'])
                    if message is not None:
                        pullsWithComments[pullSha]['authorComments'].append(message)
                else:
                    message = cleanMessage(comment['body'])
                    if message is not None:
                        pullsWithComments[pullSha]['otherComments'].append(message)

            for key in pullsWithComments.keys():
                merged = False
                authorCommentSentiment = 'neu'
                otherCommentSentiment = 'neu'
                authorComments = list(set(pullsWithComments[key]['authorComments']))
                otherComments = list(set(pullsWithComments[key]['otherComments']))

                if None in authorComments:
                    authorComments = [comment for comment in authorComments if comment is not None]
                if None in otherComments:
                    otherComments = [comment for comment in otherComments if comment is not None]

                if 'merged' in pull.keys():
                    merged = pull['merged']
                else:
                    if 'merged_at' in pull.keys():
                        if pull['merged_at'] is not None:
                            merged = True

                if len(authorComments) > 1:
                    authorCommentSentiment = getCollectiveCommentsSentiment(commentsList, authorComments, merged, False, authorName)
                if len(otherComments) > 1:
                    otherCommentSentiment = getCollectiveCommentsSentiment(commentsList, otherComments, merged, True, authorName)

                writer.writerow((key, authorCommentSentiment, otherCommentSentiment, merged))

        f.close()

    print "Both sentiments present and merged: ", bothSentimentsMerged
    print "Both sentiments present and NOT merged: ", bothSentimentsNotMerged

def getCollectiveCommentsSentiment(commentsObj, comments, merged, otherComments, authorName):
    if len(comments) < 1:
        return None

    analyzer = SentimentIntensityAnalyzer()
    collectiveSentimentList = []

    for comment in comments:
        sentiment = analyzer.polarity_scores(comment)
        sentiment.pop('compound')
        sentimentValue = max(sentiment, key=lambda i: sentiment[i])
        collectiveSentimentList.append(tuple([sentimentValue, sentiment[sentimentValue]]))

    mostPowerfulSentiment = getMostPowerfulSentiment(commentsObj, collectiveSentimentList, merged, authorName, otherComments)
    return mostPowerfulSentiment

def getMostPowerfulSentiment(commentsObj, collectiveSentimentList, merged, authorName, otherComments):
    counts = {
        'neu': 0,
        'pos': 0,
        'neg': 0
    }

    for sentiment in collectiveSentimentList:
        if sentiment[0] == 'neu':
            counts['neu'] += 1
        elif sentiment[0] == 'pos':
            counts['pos'] += 1
        elif sentiment[0] == 'neg':
            counts['neg'] += 1

    if len([senti for senti in counts.values() if senti is not 0]) > 1 and otherComments:
        if merged:
            updateSentimentDictsBasedOnMergedStatus(counts, bothSentimentsMerged)
        else:
            updateSentimentDictsBasedOnMergedStatus(counts, bothSentimentsNotMerged)

    if counts['neu'] == counts['pos'] == counts['neg']:
        return getAverages(otherComments, commentsObj, collectiveSentimentList, 'neu', 'pos', 'neg', authorName, merged)

    elif counts['pos'] < counts['neu'] and counts['neu'] == counts['neg']:
        return getAverages(otherComments, commentsObj, collectiveSentimentList, 'neu', 'neg', None, authorName, merged)

    elif counts['neg'] < counts['neu'] and counts['neu'] == counts['pos']:
        return getAverages(otherComments, commentsObj, collectiveSentimentList, 'neu', 'pos', None, authorName, merged)

    elif counts['neu'] < counts['neg'] and counts['neg'] == counts['pos']:
        return getAverages(otherComments, commentsObj, collectiveSentimentList, 'neg', 'pos', None, authorName, merged)
    else:
        return max(counts, key=lambda i: counts[i])

def getAverages(otherComments, commentsObj, collectiveSentimentList, sentiment1, sentiment2, sentiment3, authorName, merged):
    if sentiment3:
        sentimentObj = {
            sentiment1: 0,
            sentiment2: 0,
            sentiment3: 0
        }
        sentimentObj.pop(None) if None in sentimentObj.keys() else ''

        for sentiment in collectiveSentimentList:
            if sentiment[0] == sentiment1:
                sentimentObj[sentiment1] += sentiment[1]
            elif sentiment[0] == sentiment2:
                sentimentObj[sentiment2] += sentiment[1]
            elif sentiment3 and sentiment[0] == sentiment3:
                sentimentObj[sentiment3] += sentiment[1]

        if sentiment3 and sentimentObj[sentiment1] == sentimentObj[sentiment2] == sentimentObj[sentiment3]:
            if merged: bothSentimentsMerged['allThreeSameEvenAfterAverage'] += 1
            if otherComments:
                return getLastSentimentFromCommentList(commentsObj, sentimentObj, authorName)
            else:
                bothSentimentsMerged['sameEvenAfterAverageForAuthor'] += 1
                return max(sentimentObj, key=lambda i: sentimentObj[i])

        elif sentiment3 is None and sentimentObj[sentiment1] == sentimentObj[sentiment2]:
            if merged: bothSentimentsMerged['sameEvenAfterAverage'] += 1
            if all(x in sentimentObj.keys() for x in ['neg', 'neu']):
                return 'neg'
            elif all(x in sentimentObj.keys() for x in ['pos', 'neu']):
                return 'pos'
            elif all(x in sentimentObj.keys() for x in ['pos', 'neg']):
                if otherComments:
                    return getLastSentimentFromCommentList(commentsObj, sentimentObj, authorName)
                if merged: bothSentimentsMerged['posNegBothOccurredForAuthor'] += 1

        return max(sentimentObj, key=lambda i: sentimentObj[i])

def getLastSentimentFromCommentList(commentsObj, sentimentObj, authorName):
    for counter in range(len(commentsObj)-1, 0, -1):
        if commentsObj[counter]['user']['login'] is not authorName:
            sentiment = cleanAndCalculateSentimentForOne(commentsObj[counter]['body'])
            if sentiment in ['pos', 'neg']:
                return sentiment
            else:
                continue

def cleanAndCalculateSentimentForOne(comment):
    comment = cleanMessage(comment)
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(comment)
    sentiment.pop('compound')
    sentimentValue = max(sentiment, key=lambda i: sentiment[i])
    return sentimentValue

def updateSentimentDictsBasedOnMergedStatus(counts, dictToUpdate):
    if counts['pos'] > 0 and counts['neg'] > 0:
        dictToUpdate['posNeg'] += 1
    elif counts['pos'] > 0 and counts['neu'] > 0:
        dictToUpdate['posNeu'] += 1
    elif counts['neg'] > 0 and counts['neu'] > 0:
        dictToUpdate['negNeu'] += 1

def cleanMessage(m):
    m = m.replace("\n", '')
    m = m.replace("\r", '')
    m = m.replace("\t", ' ')
    m = m.replace("u'", '')
    m = m.replace(r'u"', '')
    m = re.sub('```.*```', '', m)
    m = re.sub('(?=@).*?(?=\s)', '', m)
    m = re.sub("http.* ", ' ', m)
    return m

if __name__ == '__main__':
    main()