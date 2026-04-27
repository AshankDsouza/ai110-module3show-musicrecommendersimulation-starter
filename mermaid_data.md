flowchart LR
  A[User Input<br/>genre, mood, energy, acoustic preference] --> B[Retriever<br/>PostgreSQL + pgvector similarity]
  B --> C[Recommender Agent<br/>content-based scoring + ranking]
  C --> D[LLM Summarizer<br/>one-sentence explanation]
  D --> E[Output<br/>Top recommendations + similar songs + rationale]

  E --> F[Human Review<br/>checks usefulness and bias]
  E --> G[Evaluator/Tester<br/>pytest + profile experiments]
  F --> H[Weight/Prompt Updates]
  G --> H
  H --> C
