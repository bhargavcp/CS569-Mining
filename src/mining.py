import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from githubutils import GitHub


bothSentimentsMerged = {
    'posNeg': 0,
    'posNeu': 0,
    'negNeu': 0,
    'sameEvenAfterAverage': 0,
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
    gh = GitHub('ams04', 'd972c116bb8350b56a8c2e9baee9042eb391e0a9')
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
                    authorComments.remove(None)
                if None in otherComments:
                    otherComments.remove(None)

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
#[('neu', 0.804), ('neu', 0.872), ('neu', 0.905), ('neu', 0.826), ('neu', 0.684), ('neu', 0.651), ('neu', 0.638), ('neu', 0.936), ('neu', 0.715), ('neu', 1.0), ('neu', 0.726)]

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

    if otherComments:
        if merged:
            updateBothSentimentsMergedObject(counts)
        if not merged:
            updateBothSentimentsNotMergedObject(counts)

    if counts['neu'] == counts['pos'] == counts['neg']:
        return getAverages(otherComments, commentsObj, merged, collectiveSentimentList, 'neu', None, 'pos', None, 'neg', authorName)

    elif counts['pos'] < counts['neu'] and counts['neu'] == counts['neg']:
        return getAverages(otherComments, commentsObj, merged, collectiveSentimentList, 'neu', counts['neu'], 'neg', counts['neg'], None, authorName)

    elif counts['neg'] < counts['neu'] and counts['neu'] == counts['pos']:
        return getAverages(otherComments, commentsObj, merged, collectiveSentimentList, 'neu', counts['neu'], 'pos', counts['pos'], None, authorName)

    elif counts['neu'] < counts['neg'] and counts['neg'] == counts['pos']:
        return getAverages(otherComments, commentsObj, merged, collectiveSentimentList, 'neg', counts['neg'], 'pos', counts['pos'], None, authorName)
    else:
        return max(counts, key=lambda i: counts[i])

def updateBothSentimentsMergedObject(counts):
    if counts['pos'] > 0 and counts['neg'] > 0:
        bothSentimentsMerged['posNeg'] += 1
    elif counts['pos'] > 0 and counts['neu'] > 0:
        bothSentimentsMerged['posNeu'] += 1
    elif counts['neg'] > 0 and counts['neu'] > 0:
        bothSentimentsMerged['negNeu'] += 1

def updateBothSentimentsNotMergedObject(counts):
    if counts['pos'] > 0 and counts['neg'] > 0:
        bothSentimentsNotMerged['posNeg'] += 1
    elif counts['pos'] > 0 and counts['neu'] > 0:
        bothSentimentsNotMerged['posNeu'] += 1
    elif counts['neg'] > 0 and counts['neu'] > 0:
        bothSentimentsNotMerged['negNeu'] += 1

def getAverages(otherComments, commentsObj, merged, collectiveSentimentList, sentiment1, count1 = None, sentiment2 = None, count2 = None, sentiment3 = None,
                authorName = None):
    if sentiment3:
        sentimentObj = {
            sentiment1: 0,
            sentiment2: 0,
            sentiment3: 0
        }
        for sentiment in collectiveSentimentList:
            if sentiment[0] == sentiment1:
                sentimentObj[sentiment1] += sentiment[1]
            elif sentiment[0] == sentiment2:
                sentimentObj[sentiment2] += sentiment[1]
            elif sentiment[0] == sentiment3:
                sentimentObj[sentiment3] += sentiment[1]

        if sentimentObj[sentiment1] == sentimentObj[sentiment2] == sentimentObj[sentiment3]:
            bothSentimentsMerged['sameEvenAfterAverage'] += 1
            if otherComments:
                return getLastSentimentFromCommentList(commentsObj, sentimentObj, authorName)
            else:
                print sentimentObj
                bothSentimentsMerged['sameEvenAfterAverageForAuthor'] += 1
                return max(sentimentObj, key=lambda i: sentimentObj[i])

        return max(sentimentObj, key=lambda i: sentimentObj[i])

    else:
        sentimentObj = {
            sentiment1: 0,
            sentiment2: 0
        }
        for sentiment in collectiveSentimentList:
            if sentiment[0] == sentiment1:
                sentimentObj[sentiment1] += sentiment[1]
            elif sentiment[0] == sentiment2:
                sentimentObj[sentiment2] += sentiment[1]

        if sentimentObj[sentiment1] == sentimentObj[sentiment2]:
            bothSentimentsMerged['sameEvenAfterAverage'] += 1
            if otherComments:
                if sentiment1 == 'neg' and sentiment2 == 'neu':
                    return sentiment1
                elif sentiment1 == 'neu' and sentiment2 == 'neg':
                    return sentiment2
                elif sentiment1 == 'pos' and sentiment2 == 'neu':
                    return sentiment1
                elif sentiment1 == 'neu' and sentiment2 == 'pos':
                    return sentiment2
                elif sentiment1 in ['pos', 'neg'] and sentiment2 in ['pos', 'neg']:
                    return getLastSentimentFromCommentList(commentsObj, sentimentObj, authorName)
            else:
                if sentiment1 == 'neg' and sentiment2 == 'neu':
                    return sentiment1
                elif sentiment1 == 'neu' and sentiment2 == 'neg':
                    return sentiment2
                elif sentiment1 == 'pos' and sentiment2 == 'neu':
                    return sentiment1
                elif sentiment1 == 'neu' and sentiment2 == 'pos':
                    return sentiment2
                elif sentiment1 in ['pos', 'neg'] and sentiment2 in ['pos', 'neg']:
                    bothSentimentsMerged['posNegBothOccurredForAuthor'] += 1
                    return max(sentimentObj, key=lambda i: sentimentObj[i])

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