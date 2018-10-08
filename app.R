#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#


library(ggplot2)
library(dplyr)
library(plotly)
library(shiny)

df <- read.csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv", header= TRUE)

stateList <- c("")

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("CDC Morality"),
   
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
        
        
        #Drop Down for Cause of Death
        p("Question #1"),
        selectInput('deathCauseQ1', 'Cause of Death', unique(df$ICD.Chapter), selected='"Diseases of the circulatory system"'),
        selectInput('yearQ1', 'Year', unique(df$Year), selected='2010'),
        br(),
        p("Question #2"),
        selectInput('deathCauseQ2', 'Cause of Death', unique(df$ICD.Chapter), selected='"Diseases of the circulatory system"')
      
       
        
        ),
      
      # Show a plot of the generated distribution
      mainPanel(
         plotOutput("distPlotQ1"),
         plotOutput("distPlotQ2")
         
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
   
   output$distPlotQ1 <- renderPlot({
      
     by_cause_of_death_data <- df %>%
       filter(ICD.Chapter == input$deathCauseQ1 & df$Year == input$yearQ1) %>%
       arrange(desc(Crude.Rate))
     
     by_cause_of_death_data$Crude.Rate.Rank <- rank(by_cause_of_death_data$Crude.Rate)
     
     
     
     p <- ggplot(by_cause_of_death_data, aes(x=reorder(State, -Crude.Rate.Rank),y=Crude.Rate.Rank, fill=State)) + 
       geom_bar(stat = "identity") + ggtitle(paste("Q1:", input$deathCauseQ1, " by year ", input$yearQ1 ))
     
     #output as "return"
     p + coord_flip()

   })
  
   
   
   
   output$distPlotQ2 <- renderPlot({
     
     State_Crude.Rate <- df %>%
       filter(ICD.Chapter == input$deathCauseQ2) %>%
       select(Year, State, Crude.Rate)
     
     
     
     National_Crude.Rate <-  df %>%
       filter(ICD.Chapter == input$deathCauseQ2) %>%
       group_by(Year) %>%
       summarize(Nation_death = sum(Deaths, na.rm = TRUE),Nation_popul = sum(Population, na.rm = TRUE))  %>%
       mutate(Crude.Rate = Nation_death/Nation_popul*100000)%>%
       mutate(State = "Nation")%>%
       select(Year,State,Crude.Rate)
     
     Nation_State_Crude.Rate <- rbind(National_Crude.Rate,State_Crude.Rate)
     

     
     
     randomColors <- function(x) {
       
       paste0("#",as.hexmode( round(runif(x,16,255)) ),as.hexmode( round(runif(x,16,255)) ),as.hexmode( round(runif(x,16,255)) ))
       
     } 
     
     p <- ggplot(Nation_State_Crude.Rate, aes(x=Year,y=Crude.Rate, group = State)) + 

      
       geom_line(aes(linetype=State, color=State)) +
       geom_point(aes(shape=State, color=State)) +
       
       
       ggtitle(paste("Q2:", input$deathCauseQ2, " by year" ))
     
     #output as "return"
     p 
     
   })
   
   
   
   
}

# Run the application 
shinyApp(ui = ui, server = server)

