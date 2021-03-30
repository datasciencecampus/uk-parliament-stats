library(dplyr)

#grab commons debates RDS file
filename <- file.choose()
commonsdebates <- readRDS(filename)

#check final rows for most recent date in the dataframe
tail(commonsdebates)

#change 'date' from chr to date
as.Date(commonsdebates$Date, format =  "%Y-%m-%d")

#filter out anything pre-2015 to cut down on file size
commonsdebates_2015_2019 <- filter(commonsdebates, date >= "2015-01-01")

#check filter has worked
head(commonsdebates_2015_2019)

#output as RDS & CSV
saveRDS(commonsdebates_2015_2019, "D:/uk-parliament-data/commonsdebates_2015_2019.rds")
write.csv(commonsdebates_2015_2019,"D:/uk-parliament-data/commonsdebates_2015_2019.csv", row.names = FALSE)