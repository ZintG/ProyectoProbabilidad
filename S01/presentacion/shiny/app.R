# App complementaria S01 (PROTOTIPO DOCENTE, NO PROBADA AQUÍ SIN R).
# Instalar: install.packages("shiny") ; ejecutar: shiny::runApp("shiny")
library(shiny)
ui <- fluidPage(
  titlePanel("S01 · Laboratorio interactivo de bigramas"),
  p("Aplicación Shiny: observar → contar → suavizar → predecir. No utiliza LLM."),
  sidebarLayout(sidebarPanel(
    textInput("cadena", "Cadena (alfabeto a, b, c)", value="abacabbacb"),
    sliderInput("alpha", "Suavizado aditivo α", min=0, max=3, value=1, step=.25),
    helpText("La prueba fija es abca. Se evalúan únicamente las tres transiciones.")),
    mainPanel(h4("Transiciones observadas"), verbatimTextOutput("transiciones"),
              h4("Matriz de conteos"), tableOutput("cuentas"),
              h4("Probabilidades por contexto"), tableOutput("probabilidades"),
              h4("Predicción de abca"), verbatimTextOutput("resultado"))
  )
)
server <- function(input,output,session){
  mat <- reactive({
    s <- strsplit(tolower(gsub("[[:space:]]", "",input$cadena)), "", fixed=TRUE)[[1]]
    validate(need(length(s)>=2, "Escribe al menos dos símbolos"),
             need(all(s %in% c("a","b","c")),"Solo se admiten a, b, c"))
    letras <- c("a","b","c")
    C <- matrix(0,nrow=3,ncol=3,dimnames=list(letras,letras))
    for(i in seq_len(length(s)-1L)) C[s[i],s[i+1L]] <- C[s[i],s[i+1L]]+1L
    sumas <- rowSums(C)+3*input$alpha
    P <- sweep(C+input$alpha,1,sumas,"/")
    list(C=C,P=P,s=s)
  })
  output$transiciones <- renderPrint({s<-mat()$s; print(paste(s[-length(s)],s[-1],sep=" → "))})
  output$cuentas <- renderTable({mat()$C},rownames=TRUE)
  output$probabilidades <- renderTable({round(mat()$P,4)},rownames=TRUE)
  output$resultado <- renderPrint({P<-mat()$P; z<-P["a","b"]*P["b","c"]*P["c","a"]; cat("P(abca | a inicial) =",z,"\n");cat("PPL =",if(is.finite(z)&&z>0) z^(-1/3) else Inf,"\n")})
}
shinyApp(ui,server)
