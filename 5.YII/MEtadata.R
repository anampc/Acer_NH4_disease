ID_AOI<-read.csv("ID_AOI.csv")
Treatments<-read.csv("Frag_assignments.csv")

# 6. Merge YII and sample inf and check for missing data (Optional)
ID_AOI2<-plyr::join(ID_AOI, Treatments, by =c("Genotype", "Fragment"), type="inner")

# 7. Check for missing data (Optional)
ErrorI<-dplyr::anti_join(ID_AOI, Treatments, by =c("Genotype", "Fragment"))
ErrorII<-dplyr::anti_join(Treatments, ID_AOI, by =c("Genotype", "Fragment"))

write.csv(ID_AOI2, "ID_AOI2.csv", row.names = F)
