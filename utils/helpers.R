library(RPostgres)
enc <- "UTF-8"
source(file.path(ROOT_DIR, "utils", "secret.R"), encoding = enc)

con <- dbConnect(
  Postgres(),
  dbname = dbname,
  port = port,
  user = user,
  password = password,
  host = host
)

# interested activities
dims <- c("calculus", "long_term_memory", "math_fluency", "reasoning", "processing_speed", 
          "reading", "reading", "emotion", "working_memory", "execution_speed")
names(dims) <- c("CA", "ML", "FM", "RA", "VP", "LE", "LI", "EM", "MT", "VE")

get_network_info <- function(df, q) {
  g <- graph_from_data_frame(
    df |> filter(question == q) |> select(student, value),
    directed = T
  )
  bt <- betweenness(g)
  od <- degree(g, mode = "out")
  id <- degree(g, mode = "in")
  
  cbind.data.frame(
      student_id = as.numeric(V(g)$name),
      btn = bt,
      deg_out = od,
      deg_in = id
    ) |> 
    mutate(across(-student_id, log1p))
}

to_quintile <- function(x) {
  ifelse(ceiling(x * 5) == 0, 1, ceiling(x * 5))
}
