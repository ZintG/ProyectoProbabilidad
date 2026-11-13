# S01/IC10: BPE didactico por palabra. Sin bibliotecas adicionales.
# Comparacion de longitud tokenizada en corpus SINTETICO; NO BPC ni LLM.
args <- commandArgs(trailingOnly=FALSE)
argf <- grep('^--file=',args,value=TRUE)
raiz <- if(length(argf)) dirname(dirname(normalizePath(sub('^--file=','',argf[1])))) else normalizePath('.')
D <- read.csv(file.path(raiz,'experimentos','corpus_didactico.csv'),encoding='UTF-8',stringsAsFactors=FALSE,check.names=FALSE)
normalizar <- function(x) tolower(trimws(x))
palabras <- function(s) strsplit(normalizar(s),'[[:space:]]+')[[1]]
chars <- function(s) strsplit(s,'',fixed=TRUE)[[1]]
END <- '</w>'; M <- 20L
replace_pair <- function(symbols,a,b) {
  res <- character(); i <- 1L; n <- length(symbols)
  while(i <= n) {
    if(i<n && symbols[i]==a && symbols[i+1L]==b){res<-c(res,paste0(a,b));i<-i+2L}
    else {res<-c(res,symbols[i]);i<-i+1L}
  }
  res
}
train <- function(texts,budget=M) {
  freq <- table(unlist(lapply(texts,palabras),use.names=FALSE))
  voc <- lapply(names(freq),function(w) c(chars(w),END))
  learned <- vector('list',budget)
  for(k in seq_len(budget)) {
    env <- new.env(hash=TRUE,parent=emptyenv())
    for(i in seq_along(voc)) {
      sym <- voc[[i]]; if(length(sym)<2) next
      for(j in seq_len(length(sym)-1L)) {
        key <- paste(sym[j],sym[j+1L],sep='\t')
        current <- get0(key,envir=env,ifnotfound=0L)
        assign(key,current+as.integer(freq[i]),envir=env)
      }
    }
    keys <- sort(ls(env,all.names=TRUE),method='radix')
    if(length(keys)==0L) {learned<-learned[seq_len(k-1L)];break}
    counts <- vapply(keys,function(key)get(key,envir=env,inherits=FALSE),integer(1))
    best <- keys[which.max(counts)]
    parts <- strsplit(best,'\t',fixed=TRUE)[[1]]
    learned[[k]] <- list(a=parts[1],b=parts[2],f=as.integer(max(counts)))
    voc <- lapply(voc,replace_pair,a=parts[1],b=parts[2])
  }
  learned
}
tokenizar <- function(w, learned) {
  sym <- c(chars(w),END)
  for(m in learned) sym <- replace_pair(sym,m$a,m$b)
  sym
}
contar <- function(s, learned) {
  wrd <- palabras(s)
  c(tokens=sum(vapply(wrd,function(w)length(tokenizar(w,learned)),integer(1))),palabras=length(wrd))
}
general <- D$texto[D$grupo=='general' & D$particion=='entrenamiento']
tecnico <- D$texto[D$grupo=='tecnico' & D$particion=='entrenamiento']
TEST <- D[D$particion=='prueba',,drop=FALSE]
stopifnot(length(general)==8L,length(tecnico)==8L,nrow(TEST)==6L)
mg <- train(general); mt <- train(tecnico)
stopifnot(length(mg)==M,length(mt)==M)
out <- data.frame(id=TEST$id,palabras=integer(nrow(TEST)),tokens_bpe_general=integer(nrow(TEST)),tokens_bpe_tecnico=integer(nrow(TEST)),tokens_por_palabra_general=numeric(nrow(TEST)),tokens_por_palabra_tecnico=numeric(nrow(TEST)),diferencia_tokens_por_palabra=numeric(nrow(TEST)),stringsAsFactors=FALSE)
for(i in seq_len(nrow(TEST))) {
  a<-contar(TEST$texto[i],mg);b<-contar(TEST$texto[i],mt)
  stopifnot(a['palabras']==b['palabras'])
  out$palabras[i]<-a['palabras']; out$tokens_bpe_general[i]<-a['tokens'];out$tokens_bpe_tecnico[i]<-b['tokens']
  out$tokens_por_palabra_general[i]<-round(unname(a['tokens']/a['palabras']),6)
  out$tokens_por_palabra_tecnico[i]<-round(unname(b['tokens']/b['palabras']),6)
  out$diferencia_tokens_por_palabra[i]<-round(unname((b['tokens']-a['tokens'])/a['palabras']),6)
}
write.csv(out,file.path(raiz,'experimentos','resultados_ic10_R.csv'),row.names=FALSE,fileEncoding='UTF-8')
stopifnot(sum(out$palabras)==35L)
cat('IC10 SINTETICO: tokens BPE general=',sum(out$tokens_bpe_general),' tecnico=',sum(out$tokens_bpe_tecnico),'(R ejecutado localmente; verificar paridad al elaborar el paquete)\n')
