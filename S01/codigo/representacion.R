# S01 v0.4: representaciones didácticas en R base.
# No se trata de un tokenizador neuronal ni de un corpus real.
frase <- 'el gato mira al perro'
tokens <- strsplit(frase, ' ', fixed = TRUE)[[1]]
V <- unique(tokens)
ids <- setNames(seq_along(V), V)
ngramas <- function(toks, n) {
  if (n > length(toks)) return(list())
  lapply(seq_len(length(toks)-n+1L), function(i) toks[i:(i+n-1L)])
}
one_hot <- function(token, vocabulario) as.integer(vocabulario == token)
stopifnot(length(tokens)==5L, length(ngramas(tokens,2))==4L,
          length(ngramas(tokens,3))==3L,
          identical(ngramas(tokens,2)[[1]],c('el','gato')),
          sum(one_hot('gato',V))==1L)
print(frase);print(tokens);print(ngramas(tokens,2));print(ngramas(tokens,3))
print(ids);print(one_hot('gato',V));print(table(tokens))
