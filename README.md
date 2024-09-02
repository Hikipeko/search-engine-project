## Introduction

Build a scalable search engine similar to Google or Bing, see more on https://eecs485staff.github.io/p5-search-engine/#weighted-score.

The learning goals of this project include information retrieval concepts like text analysis (tf-idf) and link analysis (PageRank), and parallel data processing with MapReduce. You’ll also gain experience using a Service-Oriented Architecture to scale dynamic pages and web search.

Create a segmented inverted index of web pages using a pipeline of MapReduce programs. Then, build an Index server, a REST API app that returns search results in JSON format. Finally, build a Search server, a user interface that returns search results just like Google or Bing.

When you’re done, you’ll have a working search engine that looks like this:

![image](https://eecs485staff.github.io/p5-search-engine/images/GUI_2.png)
