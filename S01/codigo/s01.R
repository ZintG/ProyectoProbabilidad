# S01: R base, mismos datos ilustrativos y ecuaciones que codigo/s01.py.
# Para ejecutar: Rscript codigo/s01.R (requiere instalación externa de R).
train <- strsplit('abacabbacb','',fixed=TRUE)[[1]]
test <- strsplit('abca','',fixed=TRUE)[[1]]
V <- sort(unique(c(train,test)), method='radix')
C <- matrix(0L,length(V),length(V),dimnames=list(V,V))
for (i in seq_len(length(train)-1L)) C[train[i],train[i+1L]] <- C[train[i],train[i+1L]]+1L
stopifnot(sum(C)==length(train)-1L)
transiciones <- function(C,alpha=1){
  stopifnot(alpha>=0)
  n <- rowSums(C)+alpha*ncol(C)
  if(any(n==0)) stop('contexto sin observaciones')
  sweep(C+alpha, 1, n, '/')
}
P <- transiciones(C,1)
P0 <- transiciones(C,0)
stopifnot(all(abs(rowSums(P)-1)<1e-12),
          abs(P['a','b']-3/7)<1e-12,
          abs(P['b','c']-1/6)<1e-12,
          abs(P['c','a']-2/5)<1e-12)
medir <- function(x,P,inicial=1/3){
  prob <- c(inicial,vapply(seq_len(length(x)-1),function(i) P[x[i],x[i+1]],0.0))
  bits <- if(any(prob==0)) Inf else -sum(log2(prob))
  c(bits=bits,bpc=bits/length(x),ppl=2^(bits/length(x)),eventos=length(prob))
}
stopifnot(abs(medir(test,P)['bits']-log2(105))<1e-12,is.infinite(medir(test,P0)['bits']))
H <- function(x) -sum(ifelse(x>0,x*log2(pmax(x,1e-300)),0))
KL <- function(p,q) {
  stopifnot(length(p)==length(q),all(p>=0),all(q>=0))
  if (any(p>0 & q==0)) return(Inf)
  idx <- which(p>0)
  sum(p[idx]*log2(p[idx]/q[idx]))
}
stopifnot(abs(H(c(.5,.25,.25))-1.5)<1e-12,
          abs(KL(c(.5,.25,.25),c(.25,.5,.25))-.25)<1e-12)

# BPE: pares contados por frecuencia ponderada; desempate determinista ASCII.
pesos <- c(casa=5L,casas=2L,cosa=6L,cosas=3L,caso=4L)
tokens <- lapply(names(pesos),function(w)c(strsplit(w,'',fixed=TRUE)[[1]],'<eow>'))
names(tokens) <- names(pesos)
longitud <- function() sum(vapply(names(pesos),function(w)length(tokens[[w]])*pesos[[w]],0L))
registro <- data.frame(paso=integer(),primero=character(),segundo=character(),
                       frecuencia=integer(),efectivas=integer(),longitud=integer())
for(paso in 1:6){
  f <- list()
  for(w in names(pesos)){
    z <- tokens[[w]]
    for(i in seq_len(length(z)-1L)){
      clave <- paste(z[i],z[i+1L],sep='\u241F')
      if(is.null(f[[clave]])) f[[clave]] <- 0L
      f[[clave]] <- f[[clave]]+pesos[[w]]
    }
  }
  m <- max(unlist(f))
  candidatos <- names(f)[unlist(f)==m]
  elegido <- sort(candidatos,method='radix')[1]
  par <- strsplit(elegido,'\u241F',fixed=TRUE)[[1]]
  antes <- longitud(); repes <- 0L
  for(w in names(pesos)){
    z <- tokens[[w]]; out <- character(); i <- 1L
    while(i<=length(z)){
      if(i<length(z) && identical(z[i],par[1]) && identical(z[i+1L],par[2])){
        out <- c(out,paste0(z[i],z[i+1L])); i <- i+2L; repes<-repes+pesos[[w]]
      } else {out <- c(out,z[i]); i <- i+1L}
    }
    tokens[[w]] <- out
  }
  despues <- longitud(); stopifnot(antes-despues==repes)
  registro <- rbind(registro,data.frame(paso=paso,primero=par[1],segundo=par[2],
                                       frecuencia=m,efectivas=repes,longitud=despues))
}
stopifnot(registro$longitud[1]==89,registro$longitud[6]==43)
print(C);print(P);print(medir(test,P));print(registro);print(tokens)
cat('PPL 4 eventos:',2^1.75,'; BPC A:',log2(3.2),'; BPC B:',.3*log2(25),'\n')
