"""Source of truth for the portfolio content.

Run from anywhere:  python tools/make_content.py   (writes tools/content.json)
Sources: incoming/linkedin.txt, the CV in assets/cv/, and the README of each project.
Nothing here should be added without a source.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GH = "https://github.com/abdessamadaitbrahim/"
P = []


def add(**k):
    P.append(k)


# --------------------------------------------------------------------------- projects
# Order: AI, ML and NLP first. "featured" projects appear on the home page.

add(slug="botground", title="Botground: Multilingual Sentiment Analysis", featured=True,
 short="Sentiment analysis of chatbot conversations in French, English and Moroccan Darija, with fine-tuned transformers and a Flask dashboard.",
 cats=["nlp", "dl"], stack=["PyTorch", "Hugging Face", "XLM-RoBERTa", "mBERT", "DarijaBERT", "Flask", "SQLite"],
 cover="botground/dashboard", cover_fit="cover", repo=GH + "botground-multilingual-sentiment-analysis",
 context="Internship project, Labex", experience="labex-botground",
 problem="Customer conversations handled by a chatbot arrive in French, English and Moroccan Darija written in Latin letters. Darija has no standard spelling, uses numbers as letters (3, 7), mixes with French in the same message and has few labelled resources. The goal was to score messages and whole conversations and to track customer satisfaction.",
 built=["Fine-tuned and compared three multilingual transformers on 4,199 labelled messages: XLM-RoBERTa base, mBERT and DarijaBERT, all with the same training setup (3 epochs, batch size 16, early stopping on macro F1).",
        "Three sentiment classes (negative, neutral, positive) across customer support, hospitality and logistics domains.",
        "Scored conversations message by message, with a majority vote for the conversation label and the share of positive messages as the satisfaction rate.",
        "Built a Flask dashboard that scores messages and conversations in real time and tracks satisfaction over time."],
 results=["XLM-RoBERTa base is the best model: 0.843 accuracy and 0.842 macro F1 on 840 test messages (mBERT 0.834, DarijaBERT 0.817 macro F1).",
          "The Darija specialist does not win on Darija: DarijaBERT reaches 0.832 macro F1 on Darija messages against 0.889 for XLM-RoBERTa.",
          "The training data is confidential and is not published; the repository shows aggregate statistics only."],
 gallery=[("botground/dashboard", "Botground dashboard overview", "Flask dashboard"), ("botground/models", "Model comparison", "Model comparison"), ("botground/languages", "Macro F1 by language", "Macro F1 by language"), ("botground/confusion", "Confusion matrices", "Confusion matrices")])

add(slug="emotion-recognition", title="Facial Emotion Recognition: VGG vs ResNet", featured=True,
 short="VGG and ResNet built from scratch in PyTorch on 49,779 face images. ResNet reaches 75.4% test accuracy with 34 times fewer parameters.",
 cats=["vision", "dl"], stack=["PyTorch", "CNN", "VGG", "ResNet", "Data augmentation"],
 cover="emotion/models", cover_fit="contain", repo=GH + "deep-learning-facial-emotion-recognition",
 context="Deep learning project",
 problem="Classify a face image into one of seven emotions (angry, disgust, fear, happy, neutral, sad, surprise). The aim is a fair architectural comparison: both networks are trained from scratch, with no pretrained weights, using exactly the same split, augmentation, optimizer, scheduler and number of epochs.",
 built=["Implemented a VGG-style network (five blocks, about 44.9 M parameters) and a compact residual network (about 1.30 M parameters) in PyTorch.",
        "Trained both on 49,779 grayscale images resized to 98 x 98, with a stratified 80/20 split (39,823 train, 9,956 test).",
        "Used Adam (learning rate 1e-3, weight decay 1e-4), an exponential scheduler, random flips and rotations up to 10 degrees, for 50 epochs.",
        "Analysed training curves, class imbalance and overfitting."],
 results=["ResNet: 75.4% test accuracy, 0.737 test loss. VGG: 66.7% test accuracy, 0.889 test loss.",
          "ResNet has about 34 times fewer parameters than VGG: skip connections ease gradient flow and global average pooling replaces the large fully-connected layers.",
          "ResNet overfits more (11.9-point train-test gap) but still generalises better; its test loss stops improving after about 25 epochs, so early stopping would help."],
 gallery=[("emotion/models", "VGG vs ResNet comparison", "Model comparison"), ("emotion/samples", "Samples from the dataset", "Dataset samples"), ("emotion/curves", "Training curves", "Training curves")])

add(slug="vision-vocab-tutor", title="Vision Vocab Tutor", featured=True,
 short="Learn English vocabulary from images: YOLOv8 reads the picture, a vision LLM writes the quiz, spaced repetition schedules the review.",
 cats=["vision", "nlp"], stack=["YOLOv8", "LLM (Groq, OpenRouter)", "Flask", "SQLAlchemy", "React", "Chart.js"],
 cover="vocab/home", cover_fit="cover", repo=GH + "vision-vocab-tutor",
 context="Web application",
 problem="Vocabulary is easier to remember when it is tied to what the learner can see. The application turns real-world photos into quizzes whose questions are about what is actually visible, and it brings back the words the learner gets wrong at the right time.",
 built=["An object detector (YOLOv8s, run locally) reads each picture; a vision LLM then writes a multiple-choice question about what is visible. The LLM chain uses Groq first and OpenRouter as a fallback.",
        "Four themed environments (classroom, kitchen, supermarket, fruits) and four levels, with a session of 10 questions and difficulty that adapts to the learner's results.",
        "A personal vocabulary bank with SM-2 style spaced-repetition scheduling and flashcard review sessions.",
        "A dashboard with score evolution, level distribution, per-environment statistics and a next-level prediction.",
        "Accounts with hashed passwords and a login lockout after 5 failed attempts."],
 results=[],
 gallery=[("vocab/home", "Home page", "Home"), ("vocab/dashboard", "Learner dashboard", "Dashboard"), ("vocab/bank", "Vocabulary bank", "Vocabulary bank"), ("vocab/progress", "Progress charts", "Progress charts")])

add(slug="image-captioning", title="Image Captioning on Flickr30k",
 short="Four image-to-text architectures compared with BLEU on Flickr30k, plus a Flask app that captions an uploaded image.",
 cats=["vision", "nlp", "dl"], stack=["TensorFlow", "LSTM / BiLSTM", "Transformer", "BLIP", "Flask"],
 cover="captioning/app", cover_fit="cover", repo=GH + "Deep-Learning-Based-Image-Captioning-Using-Flickr30K",
 context="Machine learning project, ENSA Tétouan, 2024-2025",
 problem="Generate a natural-language description of an image. The project compares encoder-decoder families on the Flickr30k dataset, from CNN with recurrent decoders to a Transformer decoder and the pretrained BLIP vision-language model.",
 built=["VGG19 + LSTM, InceptionV3 + BiLSTM and InceptionV3 + Transformer (6 layers, 8 heads, d = 512) trained as encoder-decoder models; BLIP used as a pretrained reference.",
        "Evaluation with BLEU-1 and BLEU-4.",
        "A Flask web application with drag-and-drop image upload (JPG and PNG up to 16 MB), model selection and caption generation. BLIP is loaded only when selected, so the app runs without PyTorch otherwise."],
 results=["BLEU-1 / BLEU-4: VGG19 + LSTM 0.5832 / 0.1720, InceptionV3 + BiLSTM 0.6037 / 0.1968, InceptionV3 + Transformer 0.6132 / 0.2114.",
          "The Transformer decoder gives the best scores among the trained models."],
 gallery=[("captioning/app", "Web application home page", "Web application"), ("captioning/examples", "Flickr30k examples", "Flickr30k examples"), ("captioning/bilstm", "InceptionV3 + BiLSTM architecture", "InceptionV3 + BiLSTM"), ("captioning/blip", "BLIP architecture", "BLIP")])

add(slug="aman-hydroponic", title="AMAN: Smart Vertical Hydroponic System",
 short="AgriTech prototype built in 48 hours at Water4Future 2026: a vertical hydroponic tower with closed-loop irrigation, a real-time IoT dashboard, the AmanBot chatbot and predictive AI.",
 cats=["embedded", "ml"], stack=["IoT sensors", "Real-time dashboard", "AI chatbot", "Predictive AI", "Solar energy"],
 cover="aman/prototype", cover_fit="cover", cover_pos="50% 62%", repo=None,
 context="Water4Future International Hackathon 2026, Montpellier, Team AMAN", hackathon="water4future-2026",
 problem="Irrigation wastes water: the team's pitch cites the FAO figure that 70% of the water used in irrigation is lost, and about 2,000 litres of water to grow 1 kg of vegetables. AMAN aims to optimise water management and make agriculture more accessible with a vertical system that recirculates its water and monitors itself.",
 built=["An AgriTech solution built in 48 hours by Team AMAN: a smart vertical hydroponic tower with closed-loop irrigation.",
        "A real-time IoT dashboard for pH, EC (electrical conductivity), temperature and solar energy.",
        "AmanBot, an AI diagnostic chatbot for crop management.",
        "Predictive AI for decision support, with solar power for energy autonomy.",
        "A pitch with a business model canvas, cost structure, financial analysis and a 6-month roadmap: prototype optimisation, pilot phase, impact measurement and preparation for deployment."],
 results=["Semi-finalist (top 38 of 125+ teams) at the Water4Future International Hackathon 2026, and winner of the jury's 2026 W4F Students Hackathon Water Talent Prize.",
          "Hackathon prototype: there is no public code repository."],
 files=[("hackathons/water4future-2026/water-talent-prize.webp", "Water Talent Prize certificate", "Image"),
        ("hackathons/water4future-2026/attestation-of-participation.webp", "Attestation of participation", "Image"),
        ("hackathons/water4future-2026/aman-presentation.pdf", "AMAN pitch presentation (French)", "PDF")],
 gallery=[("aman/prototype", "AMAN prototype: vertical hydroponic tower next to a laptop showing the monitoring dashboard", "AMAN prototype and live dashboard")])

add(slug="ctr-prediction", title="CTR Prediction: Machine Learning from Scratch",
 short="Decision Tree, Logistic Regression, Naive Bayes and SVM implemented from scratch with NumPy and compared with scikit-learn.",
 cats=["ml"], stack=["Python", "NumPy", "scikit-learn", "Pandas"],
 cover="ctr/models", cover_fit="contain", repo=GH + "ctr-prediction-ml-from-scratch",
 context="Academic project, ENSA Tétouan",
 problem="Predict whether a user clicks an online advertisement from demographic, behavioural and contextual features. The point of the project is to understand the mathematics of four classical algorithms by implementing them without a machine-learning library.",
 built=["Exploratory analysis of 10,000 rows, with 215 exact duplicates removed (9,785 left) and high-cardinality categorical features prepared for modelling.",
        "From-scratch NumPy implementations of a Decision Tree (Gini impurity, recursive best-split search), Logistic Regression (batch gradient descent), Naive Bayes and SVM.",
        "Comparison between the from-scratch models and their scikit-learn counterparts with accuracy, confusion matrices and classification reports."],
 results=["The three validated from-scratch models (Naive Bayes, Logistic Regression, SVM) reach about 0.86 test accuracy.",
          "The Decision Tree reaches about 1.00 train accuracy against about 0.82-0.83 test accuracy, a clear case of overfitting.",
          "A preprocessing bug in one scikit-learn evaluation is documented in the repository rather than hidden."],
 gallery=[("ctr/models", "Test accuracy comparison", "Model comparison"), ("ctr/eda", "Exploratory data analysis", "Distributions"), ("ctr/correlation", "Correlation heatmap", "Correlations")])

add(slug="cliffwalking", title="Value Iteration vs Policy Iteration",
 short="Dynamic programming for reinforcement learning on CliffWalking-v1: convergence, speed and optimal-policy comparison.",
 cats=["ml"], stack=["Python", "Gymnasium", "NumPy", "Reinforcement learning"],
 cover="cliffwalking/comparison", cover_fit="contain", repo=GH + "cliffwalking-value-vs-policy-iteration",
 context="Deep learning module lab, ENSA Tétouan, 2024-2025",
 problem="Compare two dynamic-programming algorithms for optimal decision-making on the 4 x 12 CliffWalking-v1 grid from Gymnasium: how fast each converges and whether they reach the same policy.",
 built=["Value Iteration with Bellman optimality updates (threshold 1e-6, at most 5,000 iterations).",
        "Policy Evaluation and Policy Iteration, with optimal policies extracted from the environment's transition model.",
        "Policy evaluation by simulation and animated trajectories of the optimal agent."],
 results=["Both algorithms converge to the same optimal policy, with a mean reward of -13.00 in about 15 iterations.",
          "Value Iteration took about 0.0094 s against about 0.3259 s for Policy Iteration, roughly 35 times faster in the recorded run (times depend on hardware)."],
 gallery=[("cliffwalking/comparison", "Comparison of the two algorithms", "Comparison")])

add(slug="ssh-log-monitoring", title="SSH Log Monitoring with AI",
 short="Real-time SSH log monitoring with Isolation Forest anomaly detection, automatic IP blocking, email alerts and a Flask dashboard.",
 cats=["ml"], stack=["Python", "Isolation Forest", "Flask", "iptables", "Linux"],
 cover="ssh/dashboard", cover_fit="cover", repo=GH + "ssh-log-monitoring-ai",
 context="Introduction to Linux course, ENSA Tétouan, 2024-2025",
 problem="Detect suspicious SSH activity as it happens instead of reading authentication logs by hand.",
 built=["Real-time monitoring of SSH authentication events from the system log.",
        "Anomaly detection on connection patterns with an Isolation Forest.",
        "Automatic blocking of suspicious IP addresses with iptables and email notifications through Gmail SMTP.",
        "A Flask web dashboard to inspect logs and run tests, with automated unit tests scheduled by cron."],
 results=["Events are stored locally in a log file; Elasticsearch is listed in the repository as a possible future improvement, not as a current feature."],
 gallery=[("ssh/dashboard", "Web dashboard", "Dashboard"), ("ssh/architecture", "System architecture", "Architecture"), ("ssh/alert", "Email alert", "Email alert")])

add(slug="scout-ai", title="Scout-AI: Football Transfer Market Intelligence",
 short="Web mining platform for football transfer potential: scraping, NLP, graph analysis, behavioural clustering and comparative machine learning.",
 cats=["nlp", "ml"], stack=["Python", "BERT", "NetworkX", "scikit-learn", "Streamlit", "MongoDB", "Neo4J", "ElasticSearch", "Docker"],
 cover="scout/models", cover_fit="contain", repo=GH + "scout-ai-web-mining",
 context="Web mining project",
 problem="Analyse the football transfer market by combining three web mining axes: content mining (press articles and player statistics), structure mining (the network of players, clubs, agents and media) and usage mining (how fans and scouts browse player profiles). The output is a transfer potential score for the 10 most prominent players in European football.",
 built=["Data collection from NewsAPI (French and English articles on 10 target players), the Football-Data API (standings, top scorers and recent results for 5 major leagues) and Transfermarkt, with ethical scraping: robots.txt check, random delays and backoff on HTTP 429.",
        "NLP on press articles: named entity recognition with CamemBERT and sentiment analysis with multilingual BERT, combined into a popularity score (0.4 x mentions + 0.35 x sentiment + 0.25 x source diversity).",
        "A NetworkX graph of players, clubs, agents, leagues and media, analysed with HITS, PageRank and Louvain community detection, and exportable to Neo4J.",
        "Usage mining on simulated web logs (500 users, 2,000 sessions): Apriori navigation patterns, K-Means audience segments (bettor, fan, curious) and Google Trends.",
        "Random Forest, SVR and Gradient Boosting compared by R² to produce a 0-100 transfer potential score in 4 categories; results stored in MongoDB, Neo4J and ElasticSearch (Docker) and explored in a 6-tab Streamlit dashboard."],
 results=["The model is trained on 100 synthetically generated players and the usage logs are simulated, so the score demonstrates the method rather than a validated prediction.",
          "Free API tiers (NewsAPI, Football-Data) limit how much live data can be collected per day."],
 gallery=[("scout/models", "Model comparison by R² score", "Model comparison")])

add(slug="paris-traffic", title="Real-Time Paris Traffic Prediction", featured=True,
 short="Streaming pipeline with Kafka, Spark Structured Streaming and Spark ML, storing predictions in MongoDB and serving a Streamlit dashboard.",
 cats=["bigdata", "ml"], stack=["Apache Kafka", "Spark Structured Streaming", "Spark ML", "MongoDB", "Streamlit"],
 cover="paris/dashboard", cover_fit="cover", repo=GH + "real-time-Paris-traffic-prediction",
 context="Academic project, ENSA Tétouan, with Ayyoub Amazal, supervised by Dr. Imad Sassi",
 problem="Urban congestion is easier to manage when conditions are monitored and anticipated. The project builds an end-to-end pipeline that ingests Paris road-traffic sensor data and predicts the traffic state in real time.",
 built=["Data from Open Data Paris: traffic flow (q) and density (k) are the input features, the traffic state is the target.",
        "Kafka ingests the JSON messages and Spark Structured Streaming parses, cleans and prepares them.",
        "Three Spark ML classifiers were trained and compared: Logistic Regression, Decision Tree and Random Forest. Logistic Regression was selected as the best-performing model and serves the stream.",
        "Predictions are persisted in MongoDB and displayed in an interactive Streamlit dashboard of traffic conditions across Paris."],
 results=[],
 gallery=[("paris/dashboard", "Streamlit dashboard", "Dashboard"), ("paris/architecture", "Pipeline architecture", "Architecture"), ("paris/models", "Model comparison", "Model comparison")])

add(slug="sportlinebot", title="SportLineBot: Field-Marking Robot",
 short="Autonomous sports-field line-marking robot on an ESP32-S3, controlled from a Flask dashboard with French NLP commands and ML anomaly detection.",
 cats=["embedded", "nlp", "ml"], stack=["ESP32-S3", "Arduino", "Flask", "Socket.IO", "scikit-learn"],
 cover="sportlinebot/dashboard", cover_fit="cover", repo=GH + "sportlinebot-field-marking-robot",
 context="MECA WORLD CUP 2026, with Abdelaaziz Ait Kheri", hackathon="meca-world-cup-2026",
 problem="Marking the lines of a sports field by hand is slow and imprecise. SportLineBot drives and sprays paint on its own while an operator supervises from a browser, with buttons or by typing a sentence in French such as \"trace un terrain de foot\".",
 built=["Firmware for an ESP32-S3 with a WebSocket server, time-based motion, an ultrasonic sensor on a servo for obstacle scanning, a paint pump and a paint-level sensor.",
        "Flask and Socket.IO dashboard with a live field view that follows the 7 steps of a football field (outer rectangle, halfway line, centre circle and both penalty and goal areas).",
        "An NLP intent classifier (TF-IDF character n-grams and Multinomial Naive Bayes, 8 intents, about 130 French phrases) that turns a sentence into a robot command.",
        "Anomaly monitoring with safety rules first (paint empty, obstacle closer than 15 cm, low paint) and an Isolation Forest second.",
        "A mock ESP32 so the dashboard can be tested without the robot."],
 results=["Hackathon prototype at reduced scale; only the football field is implemented and the motion is open loop, so it must be calibrated.",
          "The team received a certificate of participation at the MECA WORLD CUP, organised by the Club Mécatronique of ENSA Tétouan."],
 gallery=[("sportlinebot/dashboard", "SportLineBot dashboard", "Dashboard"), ("sportlinebot/robot", "SportLineBot prototype", "Prototype")])

add(slug="heart-guardian", title="Heart Guardian: ECG-Driven Adaptive Game",
 short="A wearable ESP32 ECG sensor streams the heart signal; XGBoost classifies the rhythm and a Unity game adapts in real time.",
 cats=["embedded", "ml"], stack=["ESP32", "XGBoost", "Pan-Tompkins", "Python", "Unity", "SQLite"],
 cover="heartguardian/prototype", cover_fit="cover", repo=GH + "heart-guardian-ecg-game",
 context="Game4Health Hackathon 2026, team Health Hackers", hackathon="game4health-2026",
 problem="Diabetes and obesity are rising in Morocco. Heart Guardian builds cardiac monitoring into a game so that physical activity is motivating and heart-rate anomalies are caught early.",
 built=["An ESP32 samples a 3-electrode ECG sensor at 100 Hz and streams it over WiFi.",
        "A Python pipeline detects R peaks with a Pan-Tompkins style algorithm and computes heart rate, HRV and rhythm irregularity.",
        "An XGBoost classifier trained on 10-second segments from the MIT-BIH Arrhythmia Database labels the rhythm (normal, bradycardia, tachycardia, danger); thresholds adapt to the player's age and condition.",
        "A Unity game receives one JSON result per second and adapts (normal pace, slow down, breathing pause, safe mode). Sessions, results and alerts are stored in SQLite.",
        "An ECG emulator and a Unity simulator let the project run without hardware."],
 results=["Hackathon prototype built with a business model and cost study; estimated MVP cost 2,400 to 3,500 MAD.",
          "Not a medical device: labels come from heart-rate and irregularity rules, and the system has not been clinically validated."],
 gallery=[("heartguardian/prototype", "Prototype: ESP32 and ECG electrodes", "Prototype"), ("heartguardian/architecture", "System architecture", "Architecture"), ("heartguardian/solution", "Solution overview", "Solution")])

add(slug="hadoop-sales", title="Sales Analysis with Hadoop MapReduce",
 short="Analysis of more than 4 million sales transactions with Hadoop MapReduce and Python through Hadoop Streaming.",
 cats=["bigdata"], stack=["Hadoop", "MapReduce", "HDFS", "Python", "Hadoop Streaming"],
 cover="hadoop/categories", cover_fit="contain", repo=GH + "hadoop-mapreduce-sales-analysis",
 context="Big Data project",
 problem="Aggregate a file of more than 4 million sales transactions (date, time, store, category, amount, payment method) with the MapReduce programming model.",
 built=["Python 3 mappers that extract a key (store or category) and the amount, and reducers that aggregate the pairs after Hadoop's shuffle and sort.",
        "Four analyses: sales per store, sales per category, highest sale per store, and overall total with the number of sales.",
        "Jobs run through Hadoop Streaming on HDFS, after a local test on a sample with a Unix pipe (head | mapper | sort | reducer)."],
 results=["4,138,476 transactions processed, for total sales of 1,034,457,953.26.",
          "Toys is the top category (57,463,477.11), just ahead of Consumer Electronics (57,452,374.13).",
          "Limitations documented in the repository: floating-point artefacts in sums, no combiner, and a total reducer that assumes a single reducer."],
 gallery=[("hadoop/categories", "Sales by category", "Sales by category")])

add(slug="university-dwh-bi", title="University Data Warehouse and BI",
 short="End-to-end Business Intelligence: star-schema data warehouse, SSIS ETL pipelines, SSAS OLAP cube and Power BI dashboards.",
 cats=["bi"], stack=["SQL Server", "SSIS", "SSAS", "Power BI", "T-SQL"],
 cover="dwbi/dashboard", cover_fit="cover", repo=GH + "University-Data-Warehouse-BI-Project",
 context="Business Intelligence module, ENSA Tétouan, 2025-2026",
 problem="University data is spread across several sources, which makes it hard to keep consistent and to analyse. The project covers the complete BI lifecycle: raw CSV data, ETL, data warehouse, OLAP cube and dashboards.",
 built=["An SSIS master package that removes duplicates, handles nulls, standardises dates and emails, corrects gender values, cleans names and rejects grades outside 0-20.",
        "Invalid records are redirected to an Excel file for correction and reintegration, so nothing is silently lost.",
        "A staging database, then a star-schema warehouse loaded with surrogate keys and incremental updates.",
        "An SSAS MOLAP cube with course and academic-date hierarchies (year, semester, quarter).",
        "Three Power BI dashboards: university overview, student performance and course analysis."],
 results=[],
 gallery=[("dwbi/dashboard", "Power BI dashboard", "Power BI dashboard"), ("dwbi/architecture", "Solution architecture", "Architecture")])

add(slug="power-bi-hr", title="HR Analytics Dashboard",
 short="Interactive Power BI dashboard on workforce, promotions, retrenchments and satisfaction.",
 cats=["bi"], stack=["Power BI"], cover="powerbi/overview", cover_fit="cover", repo=GH + "power-bi-hr-dashboard",
 context="Data visualisation project, with Ayyoub Amazal",
 problem="Give decision-makers a clear view of a company's workforce: gender distribution, years of service, job levels, job satisfaction, overtime, commuting distance, and the employees due for promotion or retrenchment.",
 built=["A three-page Power BI report with a side menu: overview, employee lists (due for promotion, possible retrenchment), and department and job role analysis.",
        "Filters by department, job level and job satisfaction; bar, pie and donut charts; detailed employee tables."],
 results=["1,470 employees in the dataset (882 male, 588 female).",
          "72 employees (4.9%) due for promotion and 117 (8.0%) flagged for retrenchment; 28.3% work overtime."],
 gallery=[("powerbi/overview", "Dashboard overview", "Overview")])

add(slug="tableau-science", title="Global Scientific Production Dashboard",
 short="Interactive Tableau dashboard on world scientific production, 1996-2014: documents, citations, H-index and country rankings.",
 cats=["bi"], stack=["Tableau", "Tableau Public"], cover="tableau/countries", cover_fit="cover", repo=GH + "tableau-global-scientific-production",
 demo="https://public.tableau.com/app/profile/abdessamad.ait.brahim/viz/Histoire1-Analysedelaproductionscientifique/Analysedelaproductionscientifique",
 context="Data Visualization module, Big Data and AI programme",
 problem="Tell the story of the world's scientific production between 1996 and 2014 from SCImago country indicators: documents, citations, H-index and rank.",
 built=["A Tableau Story with three dashboards: contribution of the leading countries, analysis by country (with a world production map) and an H-index overview.",
        "Interactive controls: indicator selector (documents or citations), year and size parameters, country filters and highlight actions.",
        "Published on Tableau Public."],
 results=[],
 gallery=[("tableau/countries", "Analysis by country", "Analysis by country"), ("tableau/hindex", "H-index overview", "H-index overview")])

add(slug="yelp-n8n", title="Web Scraping: Yelp and n8n",
 short="Automated Python and Selenium scraping for Yelp data analysis, plus an n8n workflow for multi-source smartphone price tracking.",
 cats=["bi", "bigdata"], stack=["Python", "Selenium", "n8n", "Docker", "Google Sheets"], cover="yelp/workflow", cover_fit="cover", repo=GH + "web-scraping-yelp-n8n",
 context="Web Analytics module, ENSA Tétouan, supervised by Dr. Imad Sassi",
 problem="Explore two complementary ways of collecting web data: programmatic scraping with code, and no-code workflow automation.",
 built=["A Selenium scraper for the 500 best-rated restaurants in Paris on Yelp, collecting reviewer information and producing a ranking of reviewer nationalities.",
        "Checkpoint-based progress saving so scraping can resume after an interruption, with randomised delays between interactions.",
        "An n8n workflow, running in Docker every 24 hours, that collects Samsung Galaxy S24 titles and prices from Jumia, Boulanger, AliExpress and Newegg with CSS selectors.",
        "Results sent automatically to Google Sheets through OAuth2."],
 results=[],
 gallery=[("yelp/workflow", "n8n workflow", "n8n workflow")])

add(slug="numerical-linear-algebra", title="Numerical Linear Algebra in Python",
 short="Linear systems (LU, Cholesky, Jacobi, Gauss-Seidel), SVD, QR and PCA with NumPy and SciPy, including image compression.",
 cats=["foundations"], stack=["Python", "NumPy", "SciPy", "Jupyter"], cover=None, label="Linear algebra", repo=GH + "numerical-linear-algebra-python",
 context="Individual project, Big Data and AI programme, ENSA Tétouan, 2024-2025",
 problem="Solve linear systems and apply matrix decompositions to data analysis with NumPy and SciPy.",
 built=["Linear systems: LU decomposition, Cholesky, Jacobi and Gauss-Seidel iterations, with an accuracy and execution-time comparison.",
        "Decompositions: SVD (reconstruction, rank-2 approximation) and QR (orthogonality check).",
        "Data analysis: principal component analysis via SVD and image compression at different ranks (k = 10, 50, 100).",
        "A theory report comparing direct and iterative methods for Ax = b and discussing SVD-based dimensionality reduction."],
 results=["Matrices and vectors are generated randomly, so numerical results change at each run."])

add(slug="cryptography", title="Symmetric and Asymmetric Cryptography",
 short="Study of AES, RSA, Diffie-Hellman and ElGamal for the Security and Cryptography course (December 2025), with a report and mind maps.",
 cats=["foundations"], stack=["AES", "RSA", "Diffie-Hellman", "ElGamal"], cover="crypto/aes", cover_fit="contain", repo=GH + "cryptography-symmetric-asymmetric-analysis",
 context="Security M232 and Cryptography course, December 2025",
 problem="Understand the fundamentals of modern cryptography: the AES symmetric cipher and the main asymmetric systems.",
 built=["Symmetric part: AES architecture, encryption and decryption rounds and the four transformations (SubBytes, ShiftRows, MixColumns, AddRoundKey); AES-128, AES-192 and AES-256 use 10, 12 and 14 rounds on 128-bit blocks.",
        "Asymmetric part: public and private keys, one-way functions, RSA (integer factorisation), Diffie-Hellman and ElGamal (discrete logarithm), and their roles in encryption, signatures and key exchange.",
        "A written report and mind maps with step-by-step numerical examples."],
 results=["Asymmetric systems need keys of 2048 bits or more, are vulnerable to quantum computers and are much slower than AES, so in practice they are combined with AES (hybrid encryption)."],
 gallery=[("crypto/aes", "AES mind map", "AES mind map")])

add(slug="dsa-cpp", title="C++ Data Structures and Algorithms",
 short="Data structures and algorithms implemented from scratch in C++17: pointers, OOP, sorting, recursion, stacks, queues, linked lists and dynamic programming.",
 cats=["foundations"], stack=["C++17", "g++"], cover=None, label="C++ DSA", repo=GH + "dsa-cpp-practice",
 context="Data Structures and Algorithms module, ENSA",
 problem="Strengthen core computer-science foundations by implementing classical data structures and algorithms from scratch.",
 built=["16 progressive topics, from basics, pointers, classes and STL vectors to arrays and searching.",
        "Sorting (bubble, selection, insertion, merge sort), recursion and dynamic programming (Fibonacci, 0/1 knapsack, LCS).",
        "Stacks (balanced parentheses), queues (including a queue built from two stacks) and singly linked lists (reversal, cycle detection).",
        "Binary trees and BSTs, graphs (BFS, DFS, connected components) and hash maps (frequency counting, Two Sum)."],
 results=[])

# --------------------------------------------------------------------------- experience (LinkedIn)
EXPERIENCE = [
 dict(id="stmicroelectronics", role="AI Engineer Intern", org="STMicroelectronics", kind="Internship",
      dates="Aug 2026 – Sep 2026", length="2 months", place="Bouskoura, Casablanca-Settat, Morocco · On-site",
      summary="Designed and built a proof-of-concept conversational agent that makes manufacturing performance data accessible in natural language, as an extension of an existing production capacity monitoring tool.",
      points=["Built a data pipeline in Python and pandas to clean, validate and transform production records into reliable performance indicators.",
              "Investigated a data quality issue with a hypothesis-driven method, ruling out several causes before finding the root cause.",
              "Designed a modular architecture: MariaDB for storage, FastAPI for a secured read-only API, and Dify to orchestrate an LLM-based agent.",
              "Wrote a strict system prompt so the agent never fabricates data and flags known data limitations before citing a value.",
              "Delivered a working demo that answers engineering questions in natural language."],
      skills=["Python", "SQL", "FastAPI", "MariaDB", "LLM agent orchestration (Dify)"],
      note="Company data is confidential; no code or documents are published."),
 dict(id="labex-botground", role="AI Engineer Intern, SaaS project Botground", org="Labex", kind="Internship",
      dates="Jun 2026 – Jul 2026", length="2 months", place="Casablanca-Settat, Morocco · On-site",
      summary="End-to-end NLP pipeline for automatic sentiment analysis of customer-chatbot conversations in Botground, a Moroccan SaaS chatbot platform.",
      points=["Fine-tuned multilingual Transformer models (XLM-RoBERTa, mBERT, DarijaBERT) for sentiment classification in French, English and Moroccan Darija, reaching 84.3% accuracy.",
              "Generated and curated a synthetic multilingual dataset of 4,000+ annotated conversations across hospitality, logistics and customer support.",
              "Designed a real-time analytics dashboard (Flask, SQLite): KPI tracking, sentiment trends, detection of problematic conversations, advanced filtering.",
              "Benchmarked the three models under identical conditions to justify the production choice.",
              "Deployed on AWS (EC2, S3)."],
      skills=["Python", "Hugging Face Transformers", "XLM-RoBERTa", "mBERT", "DarijaBERT"],
      project="botground"),
 dict(id="smartmatchrh", role="AI Engineer Intern, SmartMatchRH project", org="Cloud Marketing Hub", kind="Internship",
      dates="Jul 2025 – Aug 2025", length="2 months", place="Tangier, Morocco · On-site",
      summary="Development of SmartMatchRH, an AI solution to optimise recruitment.",
      points=["Deep learning for candidate-job scoring.",
              "Multilingual NLP for CV analysis.",
              "HR chatbot and analytics dashboard.",
              "Results: +35% matching accuracy, 85% time saved in pre-screening, 78% interview success rate, 200% more applications processed."],
      skills=["Artificial intelligence", "Multilingual NLP", "Agile methodology"]),
 dict(id="math-instructor", role="Mathematics Instructor", org="Self-employed", kind="Freelance",
      dates="Jan 2025 – Jun 2025", length="6 months", place="Tétouan, Morocco · Hybrid",
      summary="Private mathematics tutoring for high school students (Tronc Commun, 1st and 2nd year Baccalaureate, Moroccan curriculum).",
      points=["Core concepts: algebra, functions, analysis and geometry.",
              "Exercises and exam preparation, with lessons adapted to each student's level."],
      skills=["Mathematics", "Teaching", "Tutoring", "Communication", "Time management"]),
]

# --------------------------------------------------------------------------- education (LinkedIn dates)
EDUCATION = [
 dict(id="ensa-engineering", school="École Nationale des Sciences Appliquées de Tétouan (ENSA Tétouan)", logo=dict(src="img/site/ensa-logo.webp", alt="ENSA Tétouan logo", w=640, h=239),
      degree="Engineering cycle in Big Data and Artificial Intelligence", dates="Sep 2024 – Present",
      detail="Abdelmalek Essaâdi University. Final year; looking for a 6-month PFE internship starting January 2027.",
      skills=["Python", "SQL", "Machine learning", "Deep learning", "Data visualisation", "Agile management", "Trello", "Project management"]),
 dict(id="ensa-prep", school="ENSA Tétouan", logo=dict(src="img/site/ensa-logo.webp", alt="ENSA Tétouan logo", w=640, h=239),
      degree="Two-year integrated preparatory programme, engineering studies", dates="2022 – 2024",
      detail="Integrated preparatory years for engineering schools.",
      skills=["Mathematics", "Statistics", "Probability", "Algebra"]),
 dict(id="baccalaureate", school="Lycée Tarik Ibn Ziad, Kelaat M'Gouna, Tinghir", logo=dict(src="img/site/lycee-tarik-ibn-ziad.webp", alt="Lycee Tarik Ibn Ziad logo", w=382, h=152),
      degree="Scientific Baccalaureate, French option", dates="2020 – 2022",
      detail="",
      skills=["Public speaking", "Event presentation", "Teamwork", "Academic competitions"]),
]

# --------------------------------------------------------------------------- hackathons
HACKATHONS = [
 dict(slug="water4future-2026", title="Water4Future International Hackathon 2026", short="Water4Future 2026",
      date="26–27 February 2026", month="Feb 2026", place="Montpellier", start="2026-02-26", end="2026-02-27",
      org="UNESCO ICIREWARD, University of Montpellier", team="Team AMAN, representing ENSA Tétouan",
      result="Semi-finalist (top 38 of 125+ teams) and Water Talent Prize",
      summary="An international student hackathon on water: 125+ teams and 800+ students from 22 countries. Team AMAN reached the semi-finals and received the jury's Water Talent Prize.",
      description=["The Water4Future International Hackathon gathered more than 800 students from 22 countries in Montpellier on 26 and 27 February 2026, organised by the UNESCO ICIREWARD centre and the University of Montpellier.",
                   "Representing ENSA Tétouan as part of Team AMAN, we reached the top 38 semi-finalists out of 125+ teams. The jury also awarded the 2026 W4F Students Hackathon Water Talent Prize to the project Aman (27 February 2026, signed by Eric Servat, Director of the ICIREWARD UNESCO Centre)."],
      built=["An AgriTech solution built in 48 hours: a smart vertical hydroponic system with closed-loop irrigation.",
             "A real-time IoT dashboard for pH, EC, temperature and solar energy.",
             "AmanBot, an AI diagnostic chatbot for crop management.",
             "Predictive AI for decision support."],
      project="aman-hydroponic", project_note="",
      images=[("hackathons/water4future-2026/aman-prototype-demo.webp", "Abdessamad Ait Brahim seated next to the AMAN hydroponic tower and a laptop showing the monitoring dashboard", "With the AMAN prototype"),
              ("hackathons/water4future-2026/aman-prototype.webp", "AMAN prototype: vertical hydroponic tower next to a laptop showing the monitoring dashboard", "AMAN prototype and live dashboard"),
              ("hackathons/water4future-2026/water-talent-prize.webp", "2026 W4F Students Hackathon Water Talent Prize awarded to the project Aman", "Water Talent Prize"),
              ("hackathons/water4future-2026/attestation-of-participation.webp", "Attestation of participation in the Water4Future Students Hackathon, Montpellier, 27 February 2026", "Attestation of participation")],
      files=[("hackathons/water4future-2026/water-talent-prize.webp", "Water Talent Prize certificate", "Image"),
             ("hackathons/water4future-2026/attestation-of-participation.webp", "Attestation of participation", "Image"),
             ("hackathons/water4future-2026/aman-presentation.pdf", "AMAN pitch presentation (French)", "PDF")]),
 dict(slug="game4health-2026", title="Game4Health Hackathon 2026", short="Game4Health 2026",
      date="3–4 April 2026", month="Apr 2026", place="Rabat", start="2026-04-03", end="2026-04-04",
      org="SmartTech Lab, iSMAGI", team="Health Hackers, representing ENSA Tétouan",
      result="Finalist",
      summary="An innovation competition on games for health. Our team, Health Hackers, reached the final with Heart Guardian, an adaptive game driven by an ECG sensor.",
      description=["The Game4Health Hackathon is an innovation competition organised by the SmartTech Lab of iSMAGI in Rabat, held on 3 and 4 April 2026.",
                   "Our team, Health Hackers, was a finalist. We designed Heart Guardian, an adaptive health game that uses an ECG sensor (ESP32) and AI analysis of the heart rhythm, and pitched it with a full business model, cost structure and 6-month roadmap."],
      built=["An ESP32 ECG sensor streaming the heart signal over WiFi.",
             "AI analysis of the heart rhythm that classifies it in real time.",
             "A game that adapts to the player's heart rhythm.",
             "A business model, cost structure and 6-month roadmap for the pitch."],
      project="heart-guardian", project_note="",
      images=[("hackathons/game4health-2026/pitch-team-stage.webp", "Team Health Hackers on stage pitching Heart Guardian to the audience at the Game4Health Hackathon", "Team pitch on stage"),
              ("hackathons/game4health-2026/pitch-solution-slide.webp", "Abdessamad Ait Brahim presenting the Heart Guardian solution slide: ECG sensor, AI analysis, adaptive game", "Presenting the solution"),
              ("img/projects/heartguardian/prototype.webp", "Heart Guardian prototype: ESP32 and ECG electrodes", "Heart Guardian prototype"),
              ("hackathons/game4health-2026/certificate-of-participation.webp", "Game4Health team attestation of participation for Health Hackers, issued by the SmartTech Lab of iSMAGI", "Attestation of participation")],
      files=[("hackathons/game4health-2026/certificate-of-participation.webp", "Attestation of participation (team)", "Image"),
             ("hackathons/game4health-2026/heart-guardian-presentation.pdf", "Heart Guardian pitch presentation (French)", "PDF")]),
 dict(slug="meca-world-cup-2026", title="MECA WORLD CUP 2026", short="MECA WORLD CUP 2026",
      date="May 2026", month="May 2026", place="", start="2026-05", end="2026-05",
      org="Club Mécatronique, ENSA Tétouan", team="With Abdelaaziz Ait Kheri (mechatronics)",
      result="Participant, certificate of participation",
      summary="A national robotics competition. With a mechatronics teammate, I built SportLineBot, an autonomous robot that paints sports field lines from natural-language commands.",
      description=["MECA WORLD CUP 2026 is a national robotics competition organised by the Club Mécatronique of ENSA Tétouan.",
                   "With Abdelaaziz Ait Kheri (mechatronics engineering), I presented SportLineBot, an autonomous robot that paints sports field lines (football, basketball, tennis, handball) from natural-language commands. I developed the AI part."],
      built=["An NLP module (TF-IDF and Naive Bayes, about 90% accuracy) that turns French sentences into robot commands.",
             "An Isolation Forest module for real-time anomaly detection: obstacles, empty paint tank, blocked robot.",
             "Both models run locally with scikit-learn."],
      project="sportlinebot", project_note="",
      images=[("hackathons/meca-world-cup-2026/team-photo.webp", "Abdessamad Ait Brahim and teammate Abdelaaziz Ait Kheri in front of the MECA WORLD CUP 2026 sponsor wall", "With my teammate at the event"),
              ("hackathons/meca-world-cup-2026/presenting-sportlinebot.webp", "Abdessamad Ait Brahim presenting SportLineBot with a microphone", "Presenting SportLineBot"),
              ("hackathons/meca-world-cup-2026/robot-prototype.webp", "SportLineBot robot prototype with its paint tank, ESP32 board and ultrasonic sensor", "SportLineBot prototype"),
              ("hackathons/meca-world-cup-2026/user-manual-cover.webp", "Cover of the SportLineBot user manual", "User manual cover"),
              ("hackathons/meca-world-cup-2026/certificate-of-participation.webp", "MECA WORLD CUP 2026 certificate of participation, Club Mécatronique", "Certificate of participation")],
      files=[("hackathons/meca-world-cup-2026/certificate-of-participation.webp", "Certificate of participation", "Image"),
             ("hackathons/meca-world-cup-2026/sportlinebot-presentation.pdf", "SportLineBot presentation (French)", "PDF")]),
]

# --------------------------------------------------------------------------- volunteering, honors, languages
VOLUNTEERING = [
 dict(id="hand-in-hand", role="Participant, Erasmus+ Youth Exchange \"Hand in Hand\"", org="1001 Schakels", dates="Sep 2021 (8–19 September)", cause="Social services",
      text="A youth exchange between young people from Belgium and Morocco.",
      points=["Helped refurbish and equip 2 village schools (80 pupils aged 3 to 6) so they could open.",
              "Took part in workshops and debates on Amazigh identity, civic engagement, women's role in society and environmental responsibility.",
              "Practised intercultural communication and teamwork in a multicultural group, and shared the Tamazight language and culture.",
              "Certified through Youthpass."],
      certificate=dict(pdf="volunteering/youthpass-hand-in-hand-2021.pdf", preview="volunteering/youthpass-hand-in-hand-2021.webp",
                       label="Youthpass certificate", alt="First page of the Youthpass certificate for the Hand in Hand youth exchange, with the birth date line redacted",
                       note="Redacted copy: the line with my date and place of birth is removed.")),
 dict(id="amazigh-new-year", role="Active participant", org="Citizenship and Human Rights Education Club, Tarik Ibn Ziyad High School", dates="Jan 2022", cause="Education",
      text="Took an active part in the cultural evening organised to celebrate the Amazigh New Year 2972, promoting Amazigh culture and heritage.",
      points=[],
      certificate=dict(pdf="volunteering/amazigh-new-year-2022-certificate.pdf", preview="volunteering/amazigh-new-year-2022-certificate.webp",
                       label="Certificate of appreciation (Arabic)", alt="Certificate of appreciation from the Citizenship and Human Rights Education Club of Tarik Ibn Ziad High School for the Amazigh New Year 2972 evening",
                       note="")),
]

HONORS = [
 dict(title="Semi-finalist (top 38 of 125+ teams) and Water Talent Prize", event="Water4Future International Hackathon 2026",
      issuer="UNESCO ICIREWARD, University of Montpellier", date="Feb 2026", hackathon="water4future-2026",
      text="Top 38 semi-finalists out of 125+ teams and 800+ students from 22 countries, with Team AMAN. The jury also awarded the 2026 W4F Students Hackathon Water Talent Prize to the project Aman."),
 dict(title="Finalist", event="Game4Health Hackathon 2026",
      issuer="SmartTech Lab, iSMAGI, Rabat", date="Apr 2026", hackathon="game4health-2026",
      text="Finalist team Health Hackers with Heart Guardian, an adaptive health game using an ECG sensor and AI analysis of the heart rhythm."),
 dict(title="Participant, SportLineBot", event="MECA WORLD CUP 2026, national robotics competition",
      issuer="Club Mécatronique, ENSA Tétouan", date="May 2026", hackathon="meca-world-cup-2026",
      text="Autonomous sports field line-marking robot built with Abdelaaziz Ait Kheri; I developed the NLP command module and the anomaly detection."),
]

LANGUAGES = [
 ("Tamazight", "Native or bilingual proficiency", 5),
 ("Arabic", "Professional working proficiency", 4),
 ("French", "Professional working proficiency", 4),
 ("English", "Professional working proficiency", 4),
 ("Spanish", "Elementary proficiency", 1),
]

# Existing groups, checked against the CV (added: Pandas, NumPy, PySpark, prompt engineering, Dify, REST APIs).
SKILLS = [
 ("Machine learning and deep learning", ["PyTorch", "TensorFlow", "scikit-learn", "XGBoost", "Pandas", "NumPy", "Isolation Forest", "Reinforcement learning"]),
 ("NLP and LLMs", ["Hugging Face", "Transformers", "XLM-RoBERTa", "BERT fine-tuning", "LLM applications", "Prompt engineering", "Dify", "TF-IDF"]),
 ("Computer vision", ["OpenCV", "YOLOv8", "CNN: VGG, ResNet", "Image captioning", "BLIP"]),
 ("Big Data", ["Apache Spark", "PySpark", "Apache Kafka", "Hadoop MapReduce", "MongoDB", "ETL / ELT"]),
 ("Languages and databases", ["Python", "C++", "SQL", "T-SQL", "PostgreSQL", "MySQL", "MariaDB", "SQL Server", "SQLite"]),
 ("Data visualisation and BI", ["Power BI", "Tableau", "SSIS", "SSAS", "Streamlit", "Matplotlib"]),
 ("Backend and tools", ["Flask", "FastAPI", "REST APIs", "Docker", "Git and GitHub", "Linux", "AWS (EC2, S3)", "SciPy"]),
 ("Embedded and IoT", ["ESP32", "Arduino", "WebSocket", "Signal processing"]),
]

INTERESTS = [
 ("Natural language processing", "Transformers, multilingual and low-resource text"),
 ("Computer vision", "Detection, recognition, image captioning"),
 ("Deep learning", "Architectures built and compared from scratch"),
 ("Multimodal AI", "Vision and language together"),
 ("Big Data", "Streaming, distributed processing, pipelines"),
 # the three below come only from Heart Guardian, SportLineBot, AMAN (Water4Future) and the STMicroelectronics internship
 ("AI for signal processing", "ECG and sensor signals: filtering, feature extraction, classification",
  [("Heart Guardian", "projects/heart-guardian.html")]),
 ("AI and IoT", "Embedded sensors, ESP32 and real-time dashboards connected to models",
  [("Heart Guardian", "projects/heart-guardian.html"), ("SportLineBot", "projects/sportlinebot.html"), ("AMAN", "hackathons/water4future-2026.html")]),
 ("Industrial AI", "Production data, anomaly detection and decision support for industry",
  [("STMicroelectronics", "experience.html#stmicroelectronics"), ("SportLineBot", "projects/sportlinebot.html"), ("AMAN", "hackathons/water4future-2026.html")]),
]

ABOUT = dict(
 short="Final-year engineering student in Big Data and Artificial Intelligence at ENSA Tétouan, Morocco. I build reliable, data-driven AI systems and care about careful experiments and honest evaluation.",
 paragraphs=["I am a final-year engineering student in Big Data and Artificial Intelligence at ENSA Tétouan (Abdelmalek Essaâdi University), Morocco.",
             "My interests are machine learning, deep learning, computer vision, NLP and multimodal AI, with a focus on building reliable, data-driven solutions through careful experimentation and evaluation. I enjoy exploring AI research as well as real-world applications in scientific and industrial settings.",
             "I am looking for a 6-month PFE internship starting in January 2027, with a long-term goal of pursuing a PhD in AI."],
 quote="Everything will come in its time, right and fittingly.",
 facts=[("Studying", "Big Data & AI engineering, ENSA Tétouan"), ("Looking for", "6-month PFE internship, January 2027"),
        ("Long-term goal", "PhD in AI"), ("Location", "Morocco, open to international opportunities")],
)

SITE = dict(
 name="Abdessamad Ait Brahim",
 url="https://abdessamadaitbrahim.github.io",
 github="https://github.com/abdessamadaitbrahim",
 linkedin="https://www.linkedin.com/in/abdessamad-aitbrahim/",
 email_user="abdessamadaitbrahim9", email_domain="gmail.com",
 cv="assets/cv/Abdessamad_Ait_Brahim_CV.pdf",
)

# --------------------------------------------------------------------------- image sizes
S = json.loads((HERE / "img_sizes.json").read_text(encoding="utf-8"))


def size(key):
    """Project images are keyed 'dir/name'; other images by their path under assets/."""
    return S[key] if key in S else S[key.replace("img/projects/", "", 1).replace(".webp", "")]


for p in P:
    p["gallery"] = [dict(img=g[0], alt=g[1], caption=g[2], w=S[g[0]][0], h=S[g[0]][1]) for g in p.get("gallery", [])]
    p["files"] = [dict(src=f[0], label=f[1], kind=f[2]) for f in p.get("files", [])]
    if p.get("cover"):
        p["cover_w"], p["cover_h"] = S[p["cover"]]
    p.setdefault("results", [])
    p.setdefault("featured", False)
for v in VOLUNTEERING:
    c = v.get("certificate")
    if c:
        c["w"], c["h"] = S[c["preview"]]
for h in HACKATHONS:
    h["images"] = [dict(src=i[0], alt=i[1], caption=i[2], w=size(i[0])[0], h=size(i[0])[1]) for i in h["images"]]
    h["files"] = [dict(src=f[0], label=f[1], kind=f[2]) for f in h["files"]]

data = dict(site=SITE, about=ABOUT, interests=INTERESTS, skills=SKILLS, languages=LANGUAGES,
            projects=P, experience=EXPERIENCE, education=EDUCATION, hackathons=HACKATHONS,
            volunteering=VOLUNTEERING, honors=HONORS)
(HERE / "content.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(P), "projects,", len(HACKATHONS), "hackathons,", len(EXPERIENCE), "experiences")
