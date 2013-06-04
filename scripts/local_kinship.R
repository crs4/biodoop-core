# BEGIN_COPYRIGHT
# 
# Copyright (C) 2009-2013 CRS4.
# 
# This file is part of biodoop-core.
# 
# biodoop-core is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# biodoop-core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# biodoop-core.  If not, see <http://www.gnu.org/licenses/>.
# 
# END_COPYRIGHT

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
