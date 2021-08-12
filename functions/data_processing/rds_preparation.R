library(dplyr)

#grab commons debates RDS file (downloaded from: https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/L4OAKN/W2SVMF&version=1.0)
filename <- file.choose()
commonsdebates <- readRDS(filename)

#check final rows for most recent date in the dataframe
tail(commonsdebates)

#change 'date' from chr to date
commonsdebates$date <- as.Date(commonsdebates$date, format = "%Y-%m-%d")

#filter out anything pre-2015 to cut down on file size
commonsdebates_2015_2019 <- filter(commonsdebates, date >= "2015-01-01")

#check filter has worked
head(commonsdebates_2015_2019)

#output as RDS & CSV
saveRDS(commonsdebates_2015_2019, "data/commonsdebates_2015_2019.rds")
write.csv(commonsdebates_2015_2019,"data/commonsdebates_2015_2019.csv", row.names = FALSE)
