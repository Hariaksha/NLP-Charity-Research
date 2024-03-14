# https://towardsdatascience.com/linguistic-complexity-measures-for-text-nlp-e4bf664bd660
library(quanteda)
library(pacman)
library(readxl)
library(quanteda.textstats)
library(dplyr)

# Set working directory
setwd("~/Repositories/NLP Charity Research")

# Read Excel spreadsheet file
mycorpus = read_excel("data/preliminary_march_data/preliminary_data.xlsx")

# Creating a corpus or dataset/frame
mission <- corpus(mycorpus$`Mission Statement`, text_field = "text")

# Tokenisation and Remove Stop Words
tok <- tokens(mission, what = "word",
              remove_punct = TRUE,
              remove_symbols = TRUE,
              remove_numbers = TRUE,
              remove_url = TRUE,
              remove_hyphens = FALSE,
              verbose = TRUE, 
              include_docvars = TRUE)
tok <- tokens_tolower(tok)
tok <- tokens_select(tok, stopwords("english"), selection = "remove", padding = FALSE)


# Readability Section
# readability <- textstat_readability(mission, c("meanSentenceLength","meanWordSyllables", "Flesch.Kincaid", "Flesch"), remove_hyphens = TRUE,
#                                     min_sentence_length = 1, max_sentence_length = 10000,
#                                     intermediate = FALSE)

# Find Flesch-Kincaid readability scores. Lower numbers = easier to read
mycorpus$readability <- textstat_readability(mission, "Flesch.Kincaid", remove_hyphens = TRUE,
                                             min_sentence_length = 1, max_sentence_length = 10000,
                                             intermediate = FALSE)

# Find Flesch's reading ease scores. Higher numbers = easier to read
mycorpus$readability2 <- textstat_readability(mission, "Flesch", remove_hyphens = TRUE,
                                             min_sentence_length = 1, max_sentence_length = 10000,
                                             intermediate = FALSE)

# Find mean lengths of sentences (number of words / number of sentences). Note that most mission statements have less than 3 sentences.
mycorpus$readability3 <- textstat_readability(mission, "meanSentenceLength", remove_hyphens = TRUE,
                                             min_sentence_length = 1, max_sentence_length = 10000,
                                             intermediate = FALSE)

# Turn revenue column from spreadsheet to numbers from strings
as.numeric(mycorpus$Revenue)

# Optional: Remove rows where revenue is 0
mycorpus = mycorpus[mycorpus$Revenue != 0,]

# Statistical Analysis of Flesch-Kincaid score with revenue
revenue_FK = lm(mycorpus$Revenue ~ mycorpus$readability$Flesch.Kincaid)
summary(revenue_FK)

# Statistical Analysis of Flesch score with revenue
revenue_Flesch = lm(mycorpus$Revenue ~ mycorpus$readability2$Flesch)
summary(revenue_Flesch)

# Statistical Analysis of mean sentence length with revenue
revenue_MSL = lm(mycorpus$Revenue ~ mycorpus$readability3$meanSentenceLength)
summary(revenue_MSL)

plot(coef(revenue_Flesch)[2])

# data binning before making scatterplot
mycorpus %>% mutate(new_bin = cut(mycorpus$readability2$Flesch, breaks=10000000))

# Scatterplot
plot(x = mycorpus$readability2$Flesch, y = mycorpus$Revenue,
     xlab = "Flesch Readability Score",
     ylab = "Revenue",
     xlim = c(-100, 100),
     ylim = c(0,100000000),        
     main = "Revenue vs Flesch Score"
)

# Measuring Richness with Type-Token Ratio (TTR)
dfm(tok) %>% 
  textstat_lexdiv(measure = "TTR")

# Measuring Richness with Hapax Richness







