# R --batch --vanilla --args input.ph input.gt < local_kinship.R

library(GenABEL)

args <- commandArgs(trailingOnly=T)
pheno <- args[1]
geno <- args[2]

print(pheno)
print(geno)

geno.raw <- sprintf("%s.raw", geno)
convert.snp.illumina(geno, geno.raw)
data <- load.gwaa.data(pheno, geno.raw, sort=F)
k <- ibs.old(data, weight="freq")
out.fn <- sprintf("%s_R.k", geno)
write.table(k, file=out.fn, quote=F, sep="\t", row.names=F, col.names=F)
