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

# Optional: Remove rows based on revenue
mycorpus = mycorpus[mycorpus$Revenue > 0,]

# Add a new column to the dataframe with the word count for each mission statement
mycorpus <- mycorpus %>% mutate(word_count = str_count(mycorpus$`Mission Statement`, "\\S+"))

# Optional: Remove rows based on word count of unprocessed mission statements
mycorpus = mycorpus[mycorpus$word_count > 6,]

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

# Optional: Adjust data to remove outliers or correct extreme values in Flesch scores
mycorpus <- mycorpus %>% filter(mycorpus$readability2$Flesch > -1, mycorpus$readability2$Flesch < 101)

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
summary_c_MSL = coeftest(revenue_MSL, vcov = clust_states_MSL)
print(summary_c_MSL)

# plot(coef(revenue_Flesch)[2])

# Apply a logarithmic transformation to Revenue to reduce the impact of outliers
# Adding a small constant to avoid taking the log of zero
mycorpus$LogRevenue <- log(mycorpus$Revenue + 1)

# Data binning and Making a Scatter Plot with Linear Regression Line for Revenue and Flesch readability.
mycorpus_summary_Flesch <- mycorpus %>%
  mutate(Flesch_bin = cut(readability2$Flesch, breaks = seq(min(readability2$Flesch, na.rm = TRUE), max(readability2$Flesch, na.rm = TRUE), length.out = 101), include.lowest = TRUE)) %>%
  group_by(Flesch_bin) %>%
  summarise(Avg_Flesch = mean(readability2$Flesch, na.rm = TRUE), Avg_Revenue = mean(Revenue, na.rm = TRUE)) %>%
  ungroup()
ggplot(mycorpus_summary_Flesch, aes(x = Avg_Flesch, y = Avg_Revenue)) +
  geom_point() + # Add points for scatter plot
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE) +  # Add linear regression line
  labs(x = "Flesch Readability Score", y = "Revenue", title = "Revenue vs Flesch Score") +
  # xlim(-200, 300) +
  # ylim(0, 12000000000) +
  theme_minimal()  # Use minimal theme for cleaner visualization

# Data binning and Making a Scatter Plot with Linear Regression Line for Revenue and mean sentence length.
mycorpus_summary_MSL <- mycorpus %>%
  mutate(MSL_bin = cut(readability3$meanSentenceLength, breaks = seq(min(readability3$meanSentenceLength, na.rm = TRUE), max(readability3$meanSentenceLength, na.rm = TRUE), length.out = 101), include.lowest = TRUE)) %>%
  group_by(MSL_bin) %>%
  summarise(Avg_MSL = mean(readability3$meanSentenceLength, na.rm = TRUE), Avg_Revenue = mean(Revenue, na.rm = TRUE)) %>%
  ungroup()
ggplot(mycorpus_summary_MSL, aes(x = Avg_MSL, y = Avg_Revenue)) +
  geom_point() + # Add points for scatter plot
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE) +  # Add linear regression line
  labs(x = "Mean Sentence Length", y = "Revenue", title = "Revenue vs Mean Sentence Length") +
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

# Data binning and Making a Scatter Plot with Linear Regression Line for Revenue and TTR richness. make sure each bin has approximately equal number of data points.
quantile_breaks <- quantile(mycorpus$richness$TTR, probs = seq(0, 1, length.out = 101), na.rm = TRUE)
unique_breaks <- unique(quantile_breaks)
mycorpus_summary_TTR <- mycorpus %>%
  mutate(TTR_bin = cut(richness$TTR, breaks = unique_breaks, include.lowest = TRUE, labels=FALSE)) %>%
  group_by(TTR_bin) %>%
  summarise(Avg_TTR = mean(richness$TTR, na.rm = TRUE), Avg_Revenue = mean(Revenue, na.rm = TRUE)) %>%
  ungroup()
ggplot(mycorpus_summary_TTR, aes(x = Avg_TTR, y = Avg_Revenue)) +
  geom_point() + # Add points for scatter plot
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE) +  # Add linear regression line
  labs(x = "Type-Token Ratio", y = "Revenue", title = "Revenue vs Type-Token Ratio") +
  # xlim(-200, 300) +
  # ylim(0, 12000000000) +
  theme_minimal()  # Use minimal theme for cleaner visualization

# Measuring Richness with Hapax Richness
dfm_object = dfm(tok)
hapax_counts = rowSums(dfm_object == 1)
total_tokens = ntoken(dfm_object)
mycorpus$hapax_richness = hapax_counts / total_tokens

# rowSums(mycorpus$dfm == 1) %>% head()
# mycorpus$richness2 = rowSums(mycorpus$dfm == 1/ntoken(mycorpus$dfm))

# Statistical Analysis of Hapax Richness with revenue
revenue_HR = lm(mycorpus$Revenue ~ mycorpus$hapax_richness)
summary(revenue_HR)

# Statistical Analysis of Hapax Richness with revenue. Cluster by states
revenue_HR = lm(mycorpus$Revenue ~ mycorpus$hapax_richness)
clust_states_HR = vcovHC(revenue_HR, type="HC1", cluster = ~ mycorpus$State)
summary_c_HR = coeftest(revenue_HR, vcov = clust_states_HR)
print(summary_c_HR)

# Data binning and Making a Scatter Plot with Linear Regression Line for Revenue and Hapax richness. make sure each bin has approximately equal number of data points.
quantile_breaks <- quantile(mycorpus$hapax_richness, probs = seq(0, 1, length.out = 101), na.rm = TRUE)
unique_breaks <- unique(quantile_breaks)
mycorpus_summary_HR <- mycorpus %>%
  mutate(HR_bin = cut(hapax_richness, breaks = unique_breaks, include.lowest = TRUE, labels=FALSE)) %>%
  group_by(HR_bin) %>%
  summarise(Avg_HR = mean(hapax_richness, na.rm = TRUE), Avg_Revenue = mean(Revenue, na.rm = TRUE)) %>%
  ungroup()
ggplot(mycorpus_summary_HR, aes(x = Avg_HR, y = Avg_Revenue)) +
  geom_point() + # Add points for scatter plot
  geom_smooth(method = "lm", formula = y ~ x, se = FALSE) +  # Add linear regression line
  labs(x = "Hapax Richness", y = "Revenue", title = "Revenue vs Hapax Richness") +
  # xlim(-200, 300) +
  # ylim(0, 12000000000) +
  theme_minimal()  # Use minimal theme for cleaner visualization



