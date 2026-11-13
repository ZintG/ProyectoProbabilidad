# S01: la misma comparación didáctica, exclusivamente R base.
# Ejecutar desde la raiz: Rscript codigo/experimento_s01.R
# Los datos son SINTÉTICOS. No afirmamos validez externa ni equivalencia
# de generadores aleatorios entre lenguajes: el bootstrap se ENUMERA.
args <- commandArgs(trailingOnly = FALSE)
ubicacion <- grep('^--file=', args, value = TRUE)
if (length(ubicacion)) {
  raiz <- dirname(dirname(normalizePath(sub('^--file=', '', ubicacion[[1]]))))
} else raiz <- normalizePath('.')
D <- read.csv(file.path(raiz, 'experimentos', 'corpus_didactico.csv'), encoding='UTF-8', stringsAsFactors=FALSE, check.names=FALSE)
normalizar <- function(x) tolower(trimws(x))
caracteres <- function(x) strsplit(x, '', fixed=TRUE)[[1]]
GEN <- vapply(D$texto[D$grupo=='general' & D$particion=='entrenamiento'], normalizar, character(1))
TEC <- vapply(D$texto[D$grupo=='tecnico' & D$particion=='entrenamiento'], normalizar, character(1))
TEST <- D[D$particion=='prueba',,drop=FALSE]
stopifnot(length(GEN)==8L, length(TEC)==8L, nrow(TEST)==6L)
vocab <- sort(unique(unlist(lapply(c(GEN,TEC),caracteres))), method='radix')
stopifnot(length(setdiff(unique(unlist(lapply(TEST$texto,caracteres))),vocab))==0L)
BOS <- '^'; EOS <- '$'; a <- 1.0
entrenar <- function(textos) {
  objetivo <- c(vocab,EOS); contextos <- c(vocab,BOS)
  C <- matrix(0L, nrow=length(contextos), ncol=length(objetivo), dimnames=list(contextos,objetivo))
  for (txt in textos) {
    ant <- BOS
    for (s in c(caracteres(txt),EOS)) {
      C[ant,s] <- C[ant,s] + 1L
      ant <- s
    }
  }
  P <- (C + a) / (rowSums(C)+a*ncol(C))
  stopifnot(max(abs(rowSums(P)-1))<1e-12)
  P
}
pg <- entrenar(GEN); pt <- entrenar(TEC)
bits <- function(txt,P) {
  ant <- BOS; res <- 0
  for(s in c(caracteres(txt),EOS)) {
    res <- res-log2(P[ant,s]); ant <- s
  }
  res
}
N <- nrow(TEST)
bpc_general <- numeric(N); bpc_tecnico <- numeric(N); lon <- integer(N)
for (i in seq_len(N)) {
  txt <- normalizar(TEST$texto[i]); lon[i] <- length(caracteres(txt))
  bpc_general[i] <- bits(txt,pg)/lon[i]
  bpc_tecnico[i] <- bits(txt,pt)/lon[i]
}
delta <- bpc_tecnico-bpc_general
# Enumeracion exhaustiva del bootstrap pareado con reemplazo: N^N
combinaciones <- expand.grid(rep(list(seq_len(N)),N))
valores <- rowMeans(matrix(delta[as.matrix(combinaciones)], ncol=N))
ic <- unname(quantile(valores,c(.025,.975),type=7))
resultado <- data.frame(id=TEST$id, caracteres=lon,
   bpc_general=round(bpc_general,8), bpc_tecnico=round(bpc_tecnico,8),
   delta_bpc=round(delta,8))
write.csv(resultado,file.path(raiz,'experimentos','resultados_R.csv'),row.names=FALSE,fileEncoding='UTF-8',na='')
cat('SINTETICO: n=',N,' vocab=',length(vocab),' delta BPC=',round(mean(delta),8),
    ' IC bootstrap pareado enumerado=',round(ic[1],8),round(ic[2],8),'\n')
stopifnot(abs(mean(delta)-(-0.54024842))<1e-7)
stopifnot(abs(ic[1]-(-0.66770598))<1e-7,abs(ic[2]-(-0.42038147))<1e-7)
