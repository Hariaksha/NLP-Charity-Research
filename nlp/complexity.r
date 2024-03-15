# https://towardsdatascience.com/linguistic-complexity-measures-for-text-nlp-e4bf664bd660

# Load necessary packages
library(lmtest)
library(sandwich)
library(quanteda)
library(pacman)
library(stringr)
library(readxl)
library(quanteda.textstats)
library(dplyr)
library(ggplot2)

# Set working directory
setwd("~/Repositories/NLP Charity Research")

# Read Excel spreadsheet file
mycorpus = read_excel("data/preliminary_march_data/data.xlsx")

# Optional: Remove rows where revenue is 0
mycorpus = mycorpus[mycorpus$Revenue != 0,]

# Add a new column to the dataframe with the word count for each mission statement
mycorpus <- mycorpus %>% mutate(word_count = str_count(mycorpus$`Mission Statement`, "\\S+"))

# Optional: Remove rows where unprocessed mission statements have less than 3 words
mycorpus = mycorpus[mycorpus$word_count > 3,]

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

# Find Readability Metrics Section
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
# as.numeric(mycorpus$Revenue)

# Statistical Analysis of Flesch-Kincaid score with revenue
revenue_FK = lm(mycorpus$Revenue ~ mycorpus$readability$Flesch.Kincaid)
summary(revenue_FK)

# Statistical Analysis of Flesch-Kincaid score with revenue. Cluster by states
revenue_FK = lm(mycorpus$Revenue ~ mycorpus$readability$Flesch.Kincaid)
clust_states_FK = vcovHC(revenue_FK, type = "HC1", cluster = ~ mycorpus$State)
summary_c_FK = coeftest(revenue_FK, vcov = clust_states_FK)
print(summary_c_FK)

# Statistical Analysis of Flesch score with revenue.
revenue_Flesch = lm(mycorpus$Revenue ~ mycorpus$readability2$Flesch)
summary(revenue_Flesch)

# Statistical Analysis of Flesch score with revenue. Cluster by states
revenue_Flesch = lm(mycorpus$Revenue ~ mycorpus$readability2$Flesch)
clust_states_Flesch = vcovHC(revenue_Flesch, type = "HC1", cluster = ~ mycorpus$State)
summary_c_Flesch = coeftest(revenue_Flesch, vcov = clust_states_Flesch)
print(summary_c_Flesch)

# Statistical Analysis of mean sentence length with revenue
revenue_MSL = lm(mycorpus$Revenue ~ mycorpus$readability3$meanSentenceLength)
summary(revenue_MSL)

# Statistical Analysis of mean sentence length with revenue. Cluster by states
revenue_MSL = lm(mycorpus$Revenue ~ mycorpus$readability3$meanSentenceLength)
clust_states_MSL = vcovHC(revenue_MSL, type="HC1", cluster = ~ mycorpus$State)
summary_c_MSL = coeftest(revenue_Flesch, vcov = clust_states_MSL)
print(summary_c_MSL)

# plot(coef(revenue_Flesch)[2])

# data binning before making scatterplot
mycorpus <- mycorpus %>% mutate(new_bin = cut(mycorpus$readability2$Flesch, breaks=100000))

# Adjust data to remove outliers or correct extreme values
mycorpus <- mycorpus %>%
  filter(mycorpus$readability2$Flesch > -1, mycorpus$readability2$Flesch < 101)

# Apply a logarithmic transformation to Revenue to reduce the impact of outliers
# Adding a small constant to avoid taking the log of zero
mycorpus$LogRevenue <- log(mycorpus$Revenue + 1)

# Making a Scatter Plot with Linear Regression Line for Revenue and Flesch readability
# plot(x = mycorpus$readability2$Flesch, y = mycorpus$Revenue,
#      xlab = "Flesch Readability Score",
#      ylab = "Revenue",
#      xlim = c(-100, 100),
#      ylim = c(0,100000000),        
#      main = "Revenue vs Flesch Score"
# )
ggplot(mycorpus, aes(x = mycorpus$readability2$Flesch, y = LogRevenue)) +
  geom_point() + # Add points for scatter plot
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE) +  # Add linear regression line
  labs(x = "Flesch Readability Score", y = "Revenue", title = "Revenue vs Flesch Score") +
  # xlim(-200, 300) +
  # ylim(0, 12000000000) +
  theme_minimal()  # Use minimal theme for cleaner visualization

# Measuring Richness with Type-Token Ratio (TTR)
mycorpus$richness = dfm(tok) %>% textstat_lexdiv(measure = "TTR")

# Statistical Analysis of TTR with revenue
revenue_TTR = lm(mycorpus$Revenue ~ mycorpus$richness$TTR)
summary(revenue_TTR)

# Statistical Analysis of TTR with revenue. Cluster by states
revenue_TTR = lm(mycorpus$Revenue ~ mycorpus$richness$TTR)
clust_states_TTR = vcovHC(revenue_TTR, type="HC1", cluster = ~ mycorpus$State)
summary_c_TTR = coeftest(revenue_TTR, vcov = clust_states_TTR)
print(summary_c_TTR)

# Making a Scatter Plot with Linear Regression Line for Revenue and TTR richness
ggplot(mycorpus, aes(x = mycorpus$richness$TTR, y = LogRevenue)) +
  geom_point() + # Add points for scatter plot
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE) +  # Add linear regression line
  labs(x = "Flesch Readability Score", y = "Log(Revenue)", title = "Revenue vs TTR Richness Score") +
  # xlim(-200, 300) +
  # ylim(0, 12000000000) +
  theme_minimal()  # Use minimal theme for cleaner visualization



# Measuring Richness with Hapax Richness






