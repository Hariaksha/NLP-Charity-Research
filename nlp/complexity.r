library(quanteda)
library(pacman)
library(readxl)
library(quanteda.textstats)

setwd("~/Repositories/NLP Charity Research")
mycorpus = read_excel("data/preliminary_march_data/preliminary_data.xlsx")
# Creating a corpus
mission <- corpus(mycorpus$`Mission Statement`, text_field = "text")
# Tokenisation
tok <- tokens(mission, what = "word",
              remove_punct = TRUE,
              remove_symbols = TRUE,
              remove_numbers = TRUE,
              remove_url = TRUE,
              remove_hyphens = FALSE,
              verbose = TRUE, 
              include_docvars = TRUE)
tok <- tokens_tolower(tok)

# Remove Stop Words
tok <- tokens_select(tok, stopwords("english"), selection = "remove", padding = FALSE)


# Readability
# readability <- textstat_readability(mission, c("meanSentenceLength","meanWordSyllables", "Flesch.Kincaid", "Flesch"), remove_hyphens = TRUE,
#                                     min_sentence_length = 1, max_sentence_length = 10000,
#                                     intermediate = FALSE)

mycorpus$readability <- textstat_readability(mission, "Flesch.Kincaid", remove_hyphens = TRUE,
                                             min_sentence_length = 1, max_sentence_length = 10000,
                                             intermediate = FALSE)
mycorpus$readability2 <- textstat_readability(mission, "Flesch", remove_hyphens = TRUE,
                                             min_sentence_length = 1, max_sentence_length = 10000,
                                             intermediate = FALSE)
mycorpus$readability3 <- textstat_readability(mission, "meanSentenceLength", remove_hyphens = TRUE,
                                             min_sentence_length = 1, max_sentence_length = 10000,
                                             intermediate = FALSE)


as.numeric(mycorpus$Revenue)

mycorpus = mycorpus[mycorpus$Revenue != 0,]

revenuereadability = lm(mycorpus$Revenue ~ mycorpus$readability$Flesch.Kincaid)

summary(revenuereadability)

revenuereadability2 = lm(mycorpus$Revenue ~ mycorpus$readability2$Flesch)

summary(revenuereadability2)

revenuereadability3 = lm(mycorpus$Revenue ~ mycorpus$readability3$meanSentenceLength)

summary(revenuereadability3)

plot(coef(revenuereadability2)[2])

plot(x = mycorpus$readability2$Flesch, y = mycorpus$Revenue,
     xlab = "Flesch Readability Score",
     ylab = "Revenue",
     xlim = c(-100, 100),
     ylim = c(0,10000000),        
     main = "Revenue vs Flesch Score"
)

# Measuring Richness with Type-Token Ratio (TTR)
dfm(tok) %>% 
  textstat_lexdiv(measure = "TTR")

# Measuring Richness with Hapax Richness







