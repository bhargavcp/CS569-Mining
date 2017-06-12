require(readr)
javaDP <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/iluwatar_java-design-patterns.csv")
guava <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/JetBrains_kotlin.csv")
airbnb <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/airbnb_javascript.csv")
webpack <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/webpack_webpack.csv")
zappa <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/Miserlou_Zappa.csv")
statsmodels <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/statsmodels_statsmodels.csv")
tootsuite <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/tootsuite_mastodon.csv")
sass <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/sass_sass.csv")
faker <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/fzaninotto_Faker.csv")
thirty <- read.csv("/Users/eecs/PycharmProjects/CS569/src/Latest/thirtybees_thirtybees.csv")

authorMessages <- read.csv("/Users/eecs/Documents/authorMessages.csv")
reviewComments <- read.csv("/Users/eecs/Desktop/reviewComments.csv")
shapiro.test(reviewComments$Percentage)
kruskal.test(reviewComments$Percentage ~ reviewComments$Sentiment)
plot(reviewComments$Percentage~reviewComments$Sentiment)

authorPosNeu <- read.csv("/Users/eecs/Documents/authorOnlyPosNeu.csv")
commentsPosNeu <- read.csv("/Users/eecs/Downloads/commentsOnlyPosNeu.csv")

wilcox.test(authorPosNeu$Neutral, authorPosNeu$Positive, paired = T)
wilcox.test(commentsPosNeu$Neutral, commentsPosNeu$Positive, paired = T)

javaDPFrame <- as.data.frame(javaDP)
guavaFrame <- as.data.frame(guava)
airbnbFrame <- as.data.frame(airbnb)
webpackFrame <- as.data.frame(webpack)
zappaFrame <- as.data.frame(zappa)
statsmodelsFrame <- as.data.frame(statsmodels)
tootsuiteFrame <- as.data.frame(tootsuite)
sassFrame <- as.data.frame(sass)
fakerFrame <- as.data.frame(faker)
thirtyFrame <- as.data.frame(thirty)

percentagePassed = sum(javaDPFrame$merged == 'True')/length(javaDPFrame$merged)
print(percentagePassed)

percentagePassed = sum(guavaFrame$merged == 'True')/length(guavaFrame$merged)
print(percentagePassed)
percentagePassed = sum(airbnbFrame$merged == 'True')/length(airbnbFrame$merged)
print(percentagePassed)
percentagePassed = sum(webpackFrame$merged == 'True')/length(webpackFrame$merged)
print(percentagePassed)
percentagePassed = sum(zappaFrame$merged == 'True')/length(zappaFrame$merged)
print(percentagePassed)
percentagePassed = sum(statsmodelsFrame$merged == 'True')/length(statsmodelsFrame$merged)
print(percentagePassed)
percentagePassed = sum(tootsuiteFrame$merged == 'True')/length(tootsuiteFrame$merged)
print(percentagePassed)
percentagePassed = sum(sassFrame$merged == 'True')/length(sassFrame$merged)
print(percentagePassed)
percentagePassed = sum(fakerFrame$merged == 'True')/length(fakerFrame$merged)
print(percentagePassed)
percentagePassed = sum(thirtyFrame$merged == 'True')/length(thirtyFrame$merged)
print(percentagePassed)

size <- c(0,0,0,0,0,1,1,1,1,1)
percentagePassed <- c(0.70,0.62,0.85,0.80,0.63,0.32,0.76,0.67,0.52,0.85)
wilcox.test(percentagePassed ~ size, exact = T)

length(javaDPFrame$merged[javaDPFrame$comments=="neg"])
length(guavaFrame$merged[guavaFrame$comments=="neg"])
length(airbnbFrame$merged[airbnbFrame$comments=="neg"])
length(webpackFrame$merged[webpackFrame$comments=="neg"])
length(zappaFrame$merged[zappaFrame$comments=="neg"])
length(statsmodelsFrame$merged[statsmodelsFrame$comments=="neg"])
length(tootsuiteFrame$merged[tootsuiteFrame$comments=="neg"])
length(sassFrame$merged[sassFrame$comments=="neg"])
length(fakerFrame$merged[fakerFrame$comments=="neg"])
length(thirtyFrame$merged[thirtyFrame$comments=="neg"])


length(javaDPFrame$merged[javaDPFrame$comments=="neg"])
length(guavaFrame$merged[guavaFrame$comments=="neg"])
length(airbnbFrame$merged[airbnbFrame$comments=="neg"])
length(webpackFrame$merged[webpackFrame$comments=="neg"])
length(zappaFrame$merged[zappaFrame$comments=="neg"])
length(statsmodelsFrame$merged[statsmodelsFrame$comments=="neg"])
length(tootsuiteFrame$merged[tootsuiteFrame$comments=="neg"])
length(sassFrame$merged[sassFrame$comments=="neg"])
length(fakerFrame$merged[fakerFrame$comments=="neg"])
length(thirtyFrame$merged[thirtyFrame$comments=="neg"])

neg_javaDPFrame_all = javaDPFrame$merged[javaDPFrame$comments=="neg"]
neg_guavaFrame_all = guavaFrame$merged[guavaFrame$comments=="neg"]
neg_airbnbFrame_all = airbnbFrame$merged[airbnbFrame$comments=="neg"]
neg_webpackFrame_all = webpackFrame$merged[webpackFrame$comments=="neg"]
neg_zappaFrame_all = zappaFrame$merged[zappaFrame$comments=="neg"]
neg_statsmodelsFrame_all = statsmodelsFrame$merged[statsmodelsFrame$comments=="neg"]
neg_tootsuiteFrame_all = tootsuiteFrame$merged[tootsuiteFrame$comments=="neg"]
neg_sassFrame_all = sassFrame$merged[sassFrame$comments=="neg"]
neg_fakerFrame_all = fakerFrame$merged[fakerFrame$comments=="neg"]
neg_thirtyFrame_all = thirtyFrame$merged[thirtyFrame$comments=="neg"]

length(subset(neg_javaDPFrame_all, neg_javaDPFrame_all == "True"))/length(neg_javaDPFrame_all)
length(subset(neg_guavaFrame_all, neg_guavaFrame_all == "True"))/length(neg_guavaFrame_all)
length(subset(neg_airbnbFrame_all, neg_airbnbFrame_all == "True"))/length(neg_airbnbFrame_all)
length(subset(neg_webpackFrame_all, neg_webpackFrame_all == "True"))/length(neg_webpackFrame_all)
length(subset(neg_zappaFrame_all, neg_zappaFrame_all == "True"))/length(neg_zappaFrame_all)
length(subset(neg_statsmodelsFrame_all, neg_statsmodelsFrame_all == "True"))/length(neg_statsmodelsFrame_all)
length(subset(neg_tootsuiteFrame_all, neg_tootsuiteFrame_all == "True"))/length(neg_tootsuiteFrame_all)
length(subset(neg_sassFrame_all, neg_sassFrame_all == "True"))/length(neg_sassFrame_all)
length(subset(neg_fakerFrame_all, neg_fakerFrame_all == "True"))/length(neg_fakerFrame_all)
length(subset(neg_thirtyFrame_all, neg_thirtyFrame_all == "True"))/length(neg_thirtyFrame_all)


neu_javaDPFrame_all <- javaDPFrame$merged[javaDPFrame$comments=="pos"]
neu_javaDPFrame_true <- subset(neu_javaDPFrame_all,neu_javaDPFrame_all=="True")
length(neu_javaDPFrame_true)/length(neu_javaDPFrame_all)

neu_javaDPFrame_all <- guavaFrame$merged[guavaFrame$comments=="pos"]
neu_javaDPFrame_true <- subset(neu_javaDPFrame_all,neu_javaDPFrame_all=="True")
length(neu_javaDPFrame_true)/length(neu_javaDPFrame_all)

neu_javaDPFrame_all <- guavaFrame$merged[guavaFrame$comments=="neg"]
neu_javaDPFrame_true <- subset(neu_javaDPFrame_all,neu_javaDPFrame_all=="True")
length(neu_javaDPFrame_true)/length(neu_javaDPFrame_all)


fisherTable = ("
              member     merged  unmerged
              posNeu    695     124
              posNeg     15     6 
              negNeu    24     41")
fisherTableData = as.matrix(read.table(textConnection(fisherTable), header=TRUE, row.names=1))
fisher.test(fisherTableData, alternative = "two.sided")
wilcox.test(commentsPosNeu$Neutral, commentsPosNeu$Positive, paired = T)
plot(reviewComments$Percentage~reviewComments$Sentiment)
