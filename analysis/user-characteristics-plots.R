rnd_data = read.csv("../results/2016_Jan_Feb_user_sample.tsv", header = TRUE, sep = "\t", row.names=NULL) #2017_Jan_Feb_user_sample.tsv
hate_data = read.csv("../results/unique-users/2016_Jan_Feb_unq_users.tsv", header = TRUE, sep = "\t", row.names=NULL)

rnd_data <- setNames(rnd_data, c('timestamp', 'tid', 'tsource', 'uid', 'user_name', 'user_screen_name', 'user_account_start', 'replytostatus', 'replytouser', 'oid', 'ouid', 'ufollowcount', 'ufriendcount', 'ufavecount', 'uretweetcount', 'ustatuscount', 'user_listedcount', 'user_loc', 'user_timezone', 'user_geoenabled', 'user_url ', 'user_profile_img_url', 'user_default_img_bool', 'user_verified', 'user_description', 'lat', 'lng', 'mentions', 'hashtags', 'urls', 'media', 'timestamp-otimestamp', 'otimestamp', 'oufollowcount', 'oufriendcount', 'oufavecount', 'oustatuscount', 'olat', 'olng', 'tex'))
hate_data <- setNames(hate_data, c('timestamp', 'tid', 'tsource', 'uid', 'user_name', 'user_screen_name', 'user_account_start', 'replytostatus', 'replytouser', 'oid', 'ouid', 'ufollowcount', 'ufriendcount', 'ufavecount', 'uretweetcount', 'ustatuscount', 'user_listedcount', 'user_loc', 'user_timezone', 'user_geoenabled', 'user_url ', 'user_profile_img_url', 'user_default_img_bool', 'user_verified', 'user_description', 'lat', 'lng', 'mentions', 'hashtags', 'urls', 'media', 'timestamp-otimestamp', 'otimestamp', 'oufollowcount', 'oufriendcount', 'oufavecount', 'oustatuscount', 'olat', 'olng', 'tex'))

#Number of followers
install.packages("sfsmisc")
library(sfsmisc)
library("poweRlaw")

#rnd_data
m_f = conpl$new(rnd_data$ufollowcount)
est_f = estimate_xmin(m_f)
m_f$setXmin(est_f)
(est = estimate_pars(m_f))


#hate_data
m_m = conpl$new(hate_data$ufollowcount)
est_m = estimate_xmin(m_m)
m_m$setXmin(est_m)
(est = estimate_pars(m_m))


pdf("followers-powlaw-fit.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
points(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n") 
mtext("Number of Followers",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(3*10^3,10^0, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()

pdf("followers-powlaw.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, type="l", cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
lines(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n") 
mtext("Number of Followers",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(3*10^3,10^0, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()


#comp = compare_distributions(m_f, m_m)


#Listed count
# data_ <- data[which(data$user_listedcount>0),]
# listed_cnt <- data$user_listedcount[which(data$user_listedcount>0)]

m_f = conpl$new(rnd_data$user_listed_count)
est_f = estimate_xmin(m_f)
m_f$setXmin(est_f)
(est = estimate_pars(m_f))


#male
m_m = conpl$new(hate_data$user_listedcount)
est_m = estimate_xmin(m_m)
m_m$setXmin(est_m)
(est = estimate_pars(m_m))

pdf("listed-powlaw-fit.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
points(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n") 
mtext("Listed count",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(10^2,10^0, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()

pdf("listed-powlaw.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, type = "l", cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
lines(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n") 
mtext("Listed count",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(10^2,10^0, c("Random Users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()

#Retweeted count
#data_ <- data[which(!is.na(data$retweet_cnt)),]

m_f = displ$new(rnd_data$uretweetcount)
est_f = estimate_xmin(m_f)
m_f$setXmin(est_f)
(est = estimate_pars(m_f))

#hate_data
m_m = displ$new(hate_data$uretweetcount)
est_m = estimate_xmin(m_m)
m_m$setXmin(est_m)
(est = estimate_pars(m_m))

pdf("retweeted-powlaw-fit.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
points(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
mtext("Retweeted count",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(10^2,10^0, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()

pdf("retweeted-powlaw.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, type = "l", cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
lines(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
mtext("Retweeted count",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(10^2,10^0, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()

#friends
#rnd_data
m_f = conpl$new(rnd_data$ufriendcount)
est_f = estimate_xmin(m_f)
m_f$setXmin(est_f)
(est = estimate_pars(m_f))

#hate_data
m_m = conpl$hate_data(data$ufriendcount)
est_m = estimate_xmin(m_m)
m_m$setXmin(est_m)
(est = estimate_pars(m_m))

pdf("friends-powlaw-fit.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
points(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n") 
mtext("Number of Friends",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(1,10^-3, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()

pdf("friends-powlaw.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, type ="l", cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
lines(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n") 
mtext("Number of Friends",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(1,10^-3, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()


#Tweets
#data_ <- data[data$user_statuses_count>0, ]
#rnd_data
m_f = displ$new(rnd_data$ustatuscount)
est_f = estimate_xmin(m_f)
m_f$setXmin(est_f)
(est = estimate_pars(m_f))


#hate_data
m_m = conpl$new(hate_data$ustatuscount)
est_m = estimate_xmin(m_m)
m_m$setXmin(est_m)
(est = estimate_pars(m_m))


pdf("ntweets-powlaw-fit.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
points(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n") 
mtext("Number of Tweets",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(1,10^-3, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()

pdf("ntweets-powlaw.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, type = "l", cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
lines(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n", lwd=2)
#lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n") 
mtext("Number of Tweets",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(1,10^-3, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()



#account age
#data_ <- data[data$accountAge_years>0, ]
user_account_start 
#rnd_data
m_f = conpl$new(rnd_data$accountAge_years)
est_f = estimate_xmin(m_f)
m_f$setXmin(est_f)
(est = estimate_pars(m_f))

#hate_data
m_m = conpl$new(hate_data$accountAge_years)
est_m = estimate_xmin(m_m)
m_m$setXmin(est_m)
(est = estimate_pars(m_m))


pdf("age-powlaw-fit.pdf")
par(mar=c(5,6.2,2,2))
plot(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_f, cex=2,col="red",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
d = plot(m_m, draw=FALSE)
points(d$x, d$y, cex=2,col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n")
lines(m_m, col="blue",xlab="",ylab="",las=1,xaxt="n",yaxt="n") 
mtext("Account age",1,line=3,cex=3)
mtext("CCDF",2,line=4,cex=3)
legend(1,10^-3, c("Random users", "Haters"),lty=c(1,1), lwd=c(3,3), col=c("red", "blue"), bty = "n", cex=2 )
eaxis(1,at=c(1,10,10^2,10^3,10^4,10^5,10^6,10^7, 10^8,10^9,10^10 ),cex.axis=1.5)
eaxis(2,at=c(10^-15, 10^-14, 10^-13, 10^-12, 10^-11, 10^-10, 10^-9,10^-8,10^-7,10^-6,10^-5,10^-4,10^-3,10^-2,10^-1,10^0),cex.axis=1.5)
dev.off()

