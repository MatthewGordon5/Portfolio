
# Libraries
#install.packages("forecast")
library("forecast")
library("imputeTS")
library("ggplot2")


# Question 1 -------------------------------------------------------------------------------------------------------

# Loading
data_initial <- read.csv("PCE.csv", header=TRUE)

# Cleaning ------------------------------------------------------------------------

# Count missing values
sum(is.na(data_initial$PCE))

# Show rows with missing PCE values 
data_initial[is.na(data_initial$PCE), ]

# Save the data as a time series
ts_data_initial <- ts(data_initial$PCE,start=c(1959, 1), end=c(2024, 12), frequency=12)

# ACF / PACF plots
tsdisplay(ts_data_initial)

# Initial Plot
autoplot(ts_data_initial) +
  ggtitle("Raw PCE Time Series (with Missing Values)") +
  ylab("Personal Consumption Expenditure") +
  xlab("Year") +
  theme_minimal()

# Imputation
data_1<-na_interpolation(ts_data_initial)
data_2<-na_ma(ts_data_initial, k=12, weighting = "exponential")
data_3<-na_kalman(ts_data_initial)
data_4<-na_kalman(ts_data_initial, model="auto.arima")

# Comparison

autoplot(data_1)
autoplot(data_2)
autoplot(data_3)
autoplot(data_4)

# Analysis ------------------------------------------------------------------------

data = data_3

seasonplot(data)

plot(decompose(data))

plot(decompose(data, type="multiplicative"))

# Remove trend by taking 1st difference
data_no_trend = diff(data)

seasonplot(data_no_trend)

# Models  ------------------------------------------------------------------------

# Test, train split

# Training: Jan 1959 – Dec 2023
train <- window(data, end = c(2023, 12))

# Test: Jan 2024 – Dec 2024
test <- window(data, start = c(2024, 1), end = c(2024, 12))


# Naive Model ---------------------------------

naive_model <- naive(train, h = 12)

autoplot(naive_model, series = "Naïve Forecast") +
  autolayer(test, series = "Actual") +
  labs(title = "Naïve Forecast vs Actual (2024)",
       x = "Year", y = "PCE (billions)") +
  scale_colour_manual(values = c("Naïve Forecast" = "blue", "Actual" = "red"),
                      name = "Series") +
  coord_cartesian(xlim = c(2024, 2024.99)) +
  theme_minimal()

accuracy(naive_model, test)


# Exponential Smoothing Model ---------------------------------

ets_model <- ets(train)

ets_forecast <- forecast(ets_model, h = 12)

autoplot(ets_forecast, series = "ETS Forecast") +
  autolayer(test, series = "Actual") +
  labs(title = "ETS Forecast vs Actual (2024)",
       x = "Year", y = "PCE (billions)") +
  scale_colour_manual(values = c("ETS Forecast" = "blue", "Actual" = "red"),
                      name = "Series") +
  coord_cartesian(xlim = c(2024, 2024.99)) +
  theme_minimal()

accuracy(ets_forecast, test)

summary(ets_model)


# ARIMA Model ---------------------------------

arima_model <- auto.arima(train)

arima_forecast <- forecast(arima_model, h = 12)

autoplot(arima_forecast, series = "ARIMA Forecast") +
  autolayer(test, series = "Actual") +
  labs(title = "ARIMA Forecast vs Actual (2024)",
       x = "Year", y = "PCE (billions)") +
  scale_colour_manual(values = c("ARIMA Forecast" = "blue", "Actual" = "red"),
                      name = "Series") +
  coord_cartesian(xlim = c(2024, 2024.99)) +
  theme_minimal()

accuracy(arima_forecast, test)

summary(arima_model)

# Predictions  ------------------------------------------------------------------------

# Naive ---------------------------------

naive_final <- naive(data, h = 12)

# Ets ---------------------------------

ets_final <- ets(data)
ets_forecast <- forecast(ets_final, h = 12)

# ARIMA ---------------------------------

arima_final <- auto.arima(data)
arima_forecast <- forecast(arima_final, h = 12)

# Plot

autoplot(naive_final$mean, series = "Naïve") +
  autolayer(ets_forecast$mean, series = "ETS") +
  autolayer(arima_forecast$mean, series = "ARIMA") +
  labs(title = "Model Comparison Forecast for 2025",
       x = "Year", y = "PCE (billions)") +
  scale_colour_manual(values = c("Naïve" = "black", "ETS" = "blue", "ARIMA" = "red"),
                      name = "Model") +
  coord_cartesian(xlim = c(2025, 2025.99)) +
  theme_minimal()

month_names <- month.abb
forecast_table <- data.frame(
  Month = month_names,
  Naive = round(as.numeric(naive_final$mean), 2),
  ETS = round(as.numeric(ets_forecast$mean), 2),
  ARIMA = round(as.numeric(arima_forecast$mean), 2)
)

print(forecast_table)


# Question 2 -------------------------------------------------------------------------------------------------------

# Packages
library(cld2)
library(dplyr)
library(tm)
library(tokenizers)
library(textstem)
library(dplyr) # basic data manipulation
library(stringr) # package for dealing with strings
library(RColorBrewer)# package to get special theme color
library(wordcloud) # package to create wordcloud
library(topicmodels) # package for topic modelling
library(ggplot2) # basic data visualization
library(LDAvis) # LDA specific visualization 
library(servr) # interactive support for LDA visualization
library(ldatuning)

# Initial Pre Processing

hotel_data <- read.csv("HotelsData.csv", stringsAsFactors = FALSE)

# Check the names of the columns
colnames(hotel_data)

# STEP 2: Filter out neutral reviews (score = 3)
filtered_data <- hotel_data %>%
  filter(Review.score != 3)

# STEP 3: Detect language and keep only English reviews
filtered_data$language <- detect_language(filtered_data$Text.1)

english_reviews <- filtered_data %>%
  filter(language == "en")

# STEP 4: Sample 2,000 reviews
set.seed(012)  
sampled_reviews <- sample_n(english_reviews, 2000)


# STEP 5: Clean the text
sampled_reviews$Text.1 <- str_conv(sampled_reviews$Text.1, "UTF-8")
sampled_reviews$Text.1 <- gsub("�", "", sampled_reviews$Text.1)
sampled_reviews$Text.1 <- gsub("[‘’´`“”–—…•°€£¥]", "", sampled_reviews$Text.1)
sampled_reviews$Text.1 <- gsub("[‐‑‒–—−-]", " ", sampled_reviews$Text.1)
sampled_reviews$Text.1 <- gsub("²", "2", sampled_reviews$Text.1)
sampled_reviews$Text.1 <- gsub("。|，", " ", sampled_reviews$Text.1)
sampled_reviews$Text.1 <- gsub("spin-dry", "spin dry", sampled_reviews$Text.1, ignore.case = TRUE)
sampled_reviews$Text.1 <- gsub("\\s+", " ", sampled_reviews$Text.1)
sampled_reviews$Text.1 <- trimws(sampled_reviews$Text.1)
sampled_reviews$Text.1 <- gsub("[\u2010\u2011\u2012\u2013\u2014\u2212]", " ", sampled_reviews$Text.1)

# STEP 6: Split into positive and negative subsets
positive_reviews <- sampled_reviews %>% filter(Review.score >= 4)
negative_reviews <- sampled_reviews %>% filter(Review.score <= 2)

# STEP 7: CORPUS
corpus_pos <- Corpus(VectorSource(positive_reviews$Text.1))
corpus_neg <- Corpus(VectorSource(negative_reviews$Text.1))

inspect(corpus_pos[grep("spin", sapply(corpus_pos, as.character))])


# STEP 8: More cleaning
corpus_pos <- tm_map(corpus_pos, content_transformer(tolower))
corpus_pos <- tm_map(corpus_pos, removePunctuation, preserve_intra_word_contractions = FALSE)
corpus_pos <- tm_map(corpus_pos, removeNumbers)
corpus_pos <- tm_map(corpus_pos, removeWords, stopwords("en"))
corpus_pos <- tm_map(corpus_pos, stripWhitespace)
corpus_pos <- tm_map(corpus_pos, content_transformer(lemmatize_strings))

corpus_neg <- tm_map(corpus_neg, content_transformer(tolower))
corpus_neg <- tm_map(corpus_neg, removePunctuation, preserve_intra_word_contractions = FALSE)
corpus_neg <- tm_map(corpus_neg, removeNumbers)
corpus_neg <- tm_map(corpus_neg, removeWords, stopwords("en"))
corpus_neg <- tm_map(corpus_neg, stripWhitespace)
corpus_neg <- tm_map(corpus_neg, content_transformer(lemmatize_strings))

# STEP 9: DTM Pos
dtm_pos <- DocumentTermMatrix(corpus_pos)

raw.sum_pos <- apply(dtm_pos, 1, sum)
dtm_pos <- dtm_pos[raw.sum_pos != 0, ]
mat_pos <- as.matrix(dtm_pos)

# Check if "spin-dry" exists in the column names
if ("spin-dry" %in% colnames(mat_pos)) {
  # Remove the "spin-dry" column
  mat_pos <- mat_pos[, colnames(mat_pos) != "spin-dry"]
  
  # Rebuild the DTM without the term
  dtm_pos <- as.DocumentTermMatrix(mat_pos, weighting = weightTf)
}

# STEP 10: DTM Neg
dtm_neg <- DocumentTermMatrix(corpus_neg)

raw.sum_neg <- apply(dtm_neg, 1, sum)
dtm_neg <- dtm_neg[raw.sum_neg != 0, ]
mat_neg <- as.matrix(dtm_neg)

# Check if "spin-dry" exists in the column names
if ("spin-dry" %in% colnames(mat_neg)) {
  # Remove the "spin-dry" column
  mat_neg <- mat_neg[, colnames(mat_neg) != "spin-dry"]
  
  # Rebuild the DTM without the term
  dtm_neg <- as.DocumentTermMatrix(mat_neg, weighting = weightTf)
}

# STEP 11: Sort by frequency positive
term_matrix_pos <- as.matrix(dtm_pos)
term_freq_pos <- sort(colSums(term_matrix_pos), decreasing = TRUE)
head(term_freq_pos, 20)

# STEP 12: Sort by frequency negative
term_matrix_neg <- as.matrix(dtm_neg)
term_freq_neg <- sort(colSums(term_matrix_neg), decreasing = TRUE)
head(term_freq_neg, 20)

# STEP 13: Check pos
all_terms_pos <- colnames(term_matrix_pos)
grep("[0-9]", all_terms_pos, value = TRUE)         # numbers
grep("[[:punct:]]", all_terms_pos, value = TRUE)   # punctuation
grep("[A-Z]", all_terms_pos, value = TRUE)         # capitals

# STEP 14: Check neg
all_terms_neg <- colnames(term_matrix_neg)
grep("[0-9]", all_terms_neg, value = TRUE)
grep("[[:punct:]]", all_terms_neg, value = TRUE)
grep("[A-Z]", all_terms_neg, value = TRUE)

# STEP 15: Word cloud for POSITIVE reviews
wordcloud(names(term_freq_pos),
          term_freq_pos,
          max.words = 50,
          scale = c(4, 0.5),
          colors = brewer.pal(8, "Dark2"),
          random.order = FALSE)

# STEP 16: Word cloud for NEGATIVE reviews
wordcloud(names(term_freq_neg),
          term_freq_neg,
          max.words = 50,
          scale = c(4, 0.5),
          colors = brewer.pal(8, "Set1"),
          random.order = FALSE)


# STEP 17: Positive reviews analysis
set.seed(012)

# result_pos <- FindTopicsNumber(
#   dtm_pos,
#   topics = seq(from = 5, to = 20, by = 1),
#   metrics = c("Griffiths2004", "CaoJuan2009", "Arun2010"),
#   method = "Gibbs",
#   control = list(seed = 77),
#   mc.cores = 2L,
#   verbose = TRUE
# )


FindTopicsNumber_plot(result_pos)

set.seed(012)
lda_pos <- LDA(dtm_pos, k = 14, method = "Gibbs",
               control = list(seed = 1234, burnin = 1000, iter = 1000))

terms_pos <- terms(lda_pos, 10)
print(terms_pos)

topic_assignments_pos <- topics(lda_pos)
head(topic_assignments_pos)

topic_probabilities_pos <- posterior(lda_pos)$topics
head(topic_probabilities_pos)

# Calculate average topic proportions
topic_means <- colMeans(topic_probabilities_pos)

# Create a data frame for plotting
topic_df <- data.frame(
  Topic = factor(1:14),
  Prevalence = topic_means
)

# Plot
ggplot(topic_df, aes(x = Topic, y = Prevalence)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  labs(title = "Topic Prevalence in Positive Reviews",
       x = "Topic Number",
       y = "Average Proportion") +
  theme_minimal()


# STEP 18: Negative reviews analysis

set.seed(012)

# result_neg <- FindTopicsNumber(
#   dtm_neg,
#   topics = seq(from = 5, to = 20, by = 1),
#   metrics = c("Griffiths2004", "CaoJuan2009", "Arun2010"),
#   method = "Gibbs",
#   control = list(seed = 77),
#   mc.cores = 2L,
#   verbose = TRUE
# )

FindTopicsNumber_plot(result_neg)

lda_neg <- LDA(dtm_neg, k = 15, method = "Gibbs",
               control = list(seed = 1234, burnin = 1000, iter = 1000))

terms_neg <- terms(lda_neg, 10)  # Top 10 words per topic
print(terms_neg)

topic_assignments_neg <- topics(lda_neg)
head(topic_assignments_neg)

topic_probabilities_neg <- posterior(lda_neg)$topics

# Calculate average topic proportions
topic_means_neg <- colMeans(topic_probabilities_neg)

# Create a data frame for plotting
topic_df_neg <- data.frame(
  Topic = factor(1:15),
  Prevalence = topic_means_neg
)

# Plot
ggplot(topic_df_neg, aes(x = Topic, y = Prevalence)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  labs(title = "Topic Prevalence in Negative Reviews",
       x = "Topic Number",
       y = "Average Proportion") +
  theme_minimal()







