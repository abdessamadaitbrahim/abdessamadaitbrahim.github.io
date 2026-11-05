import json
GH = "https://github.com/abdessamadaitbrahim/"
P = []
def add(**k): P.append(k)

add(slug="botground", title="Botground: Multilingual Sentiment Analysis",
 short="Sentiment analysis of chatbot conversations in French, English and Moroccan Darija, with fine-tuned transformers and a Flask dashboard.",
 cats=["nlp","dl"], stack=["PyTorch","Hugging Face","XLM-RoBERTa","mBERT","DarijaBERT","Flask","SQLite"],
 cover="botground/dashboard", cover_fit="cover", repo=GH+"botground-multilingual-sentiment-analysis", detail=True,
 context="Internship project",
 problem="Customer conversations handled by a chatbot arrive in French, English and Moroccan Darija written in Latin letters. Darija has no standard spelling, uses numbers as letters (3, 7), mixes with French in the same message and has few labelled resources. The goal was to score messages and whole conversations and to track customer satisfaction.",
 built=["Fine-tuned and compared three multilingual transformers on 4,199 labelled messages: XLM-RoBERTa base, mBERT and DarijaBERT, all with the same training setup (3 epochs, batch size 16, early stopping on macro F1).",
        "Three sentiment classes (negative, neutral, positive) across customer support, hospitality and logistics domains.",
        "Scored conversations message by message, with a majority vote for the conversation label and the share of positive messages as the satisfaction rate.",
        "Built a Flask dashboard that scores messages and conversations in real time and tracks satisfaction over time."],
 results=["XLM-RoBERTa base is the best model: 0.843 accuracy and 0.842 macro F1 on 840 test messages (mBERT 0.834, DarijaBERT 0.817 macro F1).",
          "The Darija specialist does not win on Darija: DarijaBERT reaches 0.832 macro F1 on Darija messages against 0.889 for XLM-RoBERTa.",
          "The training data is confidential and is not published; the repository shows aggregate statistics only."],
 gallery=[("botground/dashboard","Botground dashboard overview","Flask dashboard"),("botground/models","Model comparison","Model comparison"),("botground/languages","Macro F1 by language","Macro F1 by language"),("botground/confusion","Confusion matrices","Confusion matrices")])

add(slug="emotion-recognition", title="Facial Emotion Recognition: VGG vs ResNet",
 short="VGG and ResNet built from scratch in PyTorch on 49,779 face images. ResNet reaches 75.4% test accuracy with 34 times fewer parameters.",
 cats=["vision","dl"], stack=["PyTorch","CNN","VGG","ResNet","Data augmentation"],
 cover="emotion/models", cover_fit="contain", repo=GH+"deep-learning-facial-emotion-recognition", detail=True,
 context="Deep learning project",
 problem="Classify a face image into one of seven emotions (angry, disgust, fear, happy, neutral, sad, surprise). The aim is a fair architectural comparison: both networks are trained from scratch, with no pretrained weights, using exactly the same split, augmentation, optimizer, scheduler and number of epochs.",
 built=["Implemented a VGG-style network (five blocks, about 44.9 M parameters) and a compact residual network (about 1.30 M parameters) in PyTorch.",
        "Trained both on 49,779 grayscale images resized to 98 x 98, with a stratified 80/20 split (39,823 train, 9,956 test).",
        "Used Adam (learning rate 1e-3, weight decay 1e-4), an exponential scheduler, random flips and rotations up to 10 degrees, for 50 epochs.",
        "Analysed training curves, class imbalance and overfitting."],
 results=["ResNet: 75.4% test accuracy, 0.737 test loss. VGG: 66.7% test accuracy, 0.889 test loss.",
          "ResNet has about 34 times fewer parameters than VGG: skip connections ease gradient flow and global average pooling replaces the large fully-connected layers.",
          "ResNet overfits more (11.9-point train-test gap) but still generalises better; its test loss stops improving after about 25 epochs, so early stopping would help."],
 gallery=[("emotion/models","VGG vs ResNet comparison","Model comparison"),("emotion/samples","Samples from the dataset","Dataset samples"),("emotion/curves","Training curves","Training curves")])

add(slug="vision-vocab-tutor", title="Vision Vocab Tutor",
 short="Learn English vocabulary from images: YOLOv8 reads the picture, a vision LLM writes the quiz, spaced repetition schedules the review.",
 cats=["vision","nlp"], stack=["YOLOv8","LLM (Groq, OpenRouter)","Flask","SQLAlchemy","React","Chart.js"],
 cover="vocab/home", cover_fit="cover", repo=GH+"vision-vocab-tutor", detail=True,
 context="Web application",
 problem="Vocabulary is easier to remember when it is tied to what the learner can see. The application turns real-world photos into quizzes whose questions are about what is actually visible, and it brings back the words the learner gets wrong at the right time.",
 built=["An object detector (YOLOv8s, run locally) reads each picture; a vision LLM then writes a multiple-choice question about what is visible. The LLM chain uses Groq first and OpenRouter as a fallback.",
        "Four themed environments (classroom, kitchen, supermarket, fruits) and four levels, with a session of 10 questions and difficulty that adapts to the learner's results.",
        "A personal vocabulary bank with SM-2 style spaced-repetition scheduling and flashcard review sessions.",
        "A dashboard with score evolution, level distribution, per-environment statistics and a next-level prediction.",
        "Accounts with hashed passwords and a login lockout after 5 failed attempts."],
 results=[],
 gallery=[("vocab/home","Home page","Home"),("vocab/dashboard","Learner dashboard","Dashboard"),("vocab/bank","Vocabulary bank","Vocabulary bank"),("vocab/progress","Progress charts","Progress charts")])

add(slug="image-captioning", title="Image Captioning on Flickr30k",
 short="Four image-to-text architectures compared with BLEU on Flickr30k, plus a Flask app that captions an uploaded image.",
 cats=["vision","nlp","dl"], stack=["TensorFlow","LSTM / BiLSTM","Transformer","BLIP","Flask"],
 cover="captioning/app", cover_fit="cover", repo=GH+"Deep-Learning-Based-Image-Captioning-Using-Flickr30K", detail=True,
 context="Machine learning project, ENSA Tétouan, 2024-2025",
 problem="Generate a natural-language description of an image. The project compares encoder-decoder families on the Flickr30k dataset, from CNN with recurrent decoders to a Transformer decoder and the pretrained BLIP vision-language model.",
 built=["VGG19 + LSTM, InceptionV3 + BiLSTM and InceptionV3 + Transformer (6 layers, 8 heads, d = 512) trained as encoder-decoder models; BLIP used as a pretrained reference.",
        "Evaluation with BLEU-1 and BLEU-4.",
        "A Flask web application with drag-and-drop image upload (JPG and PNG up to 16 MB), model selection and caption generation. BLIP is loaded only when selected, so the app runs without PyTorch otherwise."],
 results=["BLEU-1 / BLEU-4: VGG19 + LSTM 0.5832 / 0.1720, InceptionV3 + BiLSTM 0.6037 / 0.1968, InceptionV3 + Transformer 0.6132 / 0.2114.",
          "The Transformer decoder gives the best scores among the trained models."],
 gallery=[("captioning/app","Web application home page","Web application"),("captioning/examples","Flickr30k examples","Flickr30k examples"),("captioning/bilstm","InceptionV3 + BiLSTM architecture","InceptionV3 + BiLSTM"),("captioning/blip","BLIP architecture","BLIP")])

add(slug="ctr-prediction", title="CTR Prediction: Machine Learning from Scratch",
 short="Decision Tree, Logistic Regression, Naive Bayes and SVM implemented from scratch with NumPy and compared with scikit-learn.",
 cats=["ml"], stack=["Python","NumPy","scikit-learn","Pandas"],
 cover="ctr/models", cover_fit="contain", repo=GH+"ctr-prediction-ml-from-scratch", detail=True,
 context="Academic project, ENSA Tétouan",
 problem="Predict whether a user clicks an online advertisement from demographic, behavioural and contextual features. The point of the project is to understand the mathematics of four classical algorithms by implementing them without a machine-learning library.",
 built=["Exploratory analysis of 10,000 rows, with 215 exact duplicates removed (9,785 left) and high-cardinality categorical features prepared for modelling.",
        "From-scratch NumPy implementations of a Decision Tree (Gini impurity, recursive best-split search), Logistic Regression (batch gradient descent), Naive Bayes and SVM.",
        "Comparison between the from-scratch models and their scikit-learn counterparts with accuracy, confusion matrices and classification reports."],
 results=["The three validated from-scratch models (Naive Bayes, Logistic Regression, SVM) reach about 0.86 test accuracy.",
          "The Decision Tree reaches about 1.00 train accuracy against about 0.82-0.83 test accuracy, a clear case of overfitting.",
          "A preprocessing bug in one scikit-learn evaluation is documented in the repository rather than hidden."],
 gallery=[("ctr/models","Test accuracy comparison","Model comparison"),("ctr/eda","Exploratory data analysis","Distributions"),("ctr/correlation","Correlation heatmap","Correlations")])

add(slug="cliffwalking", title="Value Iteration vs Policy Iteration",
 short="Dynamic programming for reinforcement learning on CliffWalking-v1: convergence, speed and optimal-policy comparison.",
 cats=["ml"], stack=["Python","Gymnasium","NumPy","Reinforcement learning"],
 cover="cliffwalking/comparison", cover_fit="contain", repo=GH+"cliffwalking-value-vs-policy-iteration", detail=True,
 context="Deep learning module lab, ENSA Tétouan, 2024-2025",
 problem="Compare two dynamic-programming algorithms for optimal decision-making on the 4 x 12 CliffWalking-v1 grid from Gymnasium: how fast each converges and whether they reach the same policy.",
 built=["Value Iteration with Bellman optimality updates (threshold 1e-6, at most 5,000 iterations).",
        "Policy Evaluation and Policy Iteration, with optimal policies extracted from the environment's transition model.",
        "Policy evaluation by simulation and animated trajectories of the optimal agent."],
 results=["Both algorithms converge to the same optimal policy, with a mean reward of -13.00 in about 15 iterations.",
          "Value Iteration took about 0.0094 s against about 0.3259 s for Policy Iteration, roughly 35 times faster in the recorded run (times depend on hardware)."],
 gallery=[("cliffwalking/comparison","Comparison of the two algorithms","Comparison")])

add(slug="ssh-log-monitoring", title="SSH Log Monitoring with AI",
 short="Real-time SSH log monitoring with Isolation Forest anomaly detection, automatic IP blocking, email alerts and a Flask dashboard.",
 cats=["ml"], stack=["Python","Isolation Forest","Flask","iptables","Linux"],
 cover="ssh/dashboard", cover_fit="cover", repo=GH+"ssh-log-monitoring-ai", detail=True,
 context="Introduction to Linux course, ENSA Tétouan, 2024-2025",
 problem="Detect suspicious SSH activity as it happens instead of reading authentication logs by hand.",
 built=["Real-time monitoring of SSH authentication events from the system log.",
        "Anomaly detection on connection patterns with an Isolation Forest.",
        "Automatic blocking of suspicious IP addresses with iptables and email notifications through Gmail SMTP.",
        "A Flask web dashboard to inspect logs and run tests, with automated unit tests scheduled by cron."],
 results=["Events are stored locally in a log file; Elasticsearch is listed in the repository as a possible future improvement, not as a current feature."],
 gallery=[("ssh/dashboard","Web dashboard","Dashboard"),("ssh/architecture","System architecture","Architecture"),("ssh/alert","Email alert","Email alert")])

add(slug="scout-ai", title="Scout-AI: Football Transfer Market Intelligence",
 short="Web mining platform for football transfer potential: scraping, NLP, graph analysis, behavioural clustering and comparative machine learning.",
 cats=["nlp","ml"], stack=["Python","NLP","Graph analysis","Streamlit","Docker"],
 cover="scout/models", cover_fit="contain", repo=GH+"scout-ai-web-mining", detail=False)

add(slug="paris-traffic", title="Real-Time Paris Traffic Prediction",
 short="Streaming pipeline with Kafka, Spark Structured Streaming and Spark ML, storing predictions in MongoDB and serving a Streamlit dashboard.",
 cats=["bigdata","ml"], stack=["Apache Kafka","Spark Structured Streaming","Spark ML","MongoDB","Streamlit"],
 cover="paris/dashboard", cover_fit="cover", repo=GH+"real-time-Paris-traffic-prediction", detail=True,
 context="Academic project, ENSA Tétouan, with Ayyoub Amazal, supervised by Dr. Imad Sassi",
 problem="Urban congestion is easier to manage when conditions are monitored and anticipated. The project builds an end-to-end pipeline that ingests Paris road-traffic sensor data and predicts the traffic state in real time.",
 built=["Data from Open Data Paris: traffic flow (q) and density (k) are the input features, the traffic state is the target.",
        "Kafka ingests the JSON messages and Spark Structured Streaming parses, cleans and prepares them.",
        "Three Spark ML classifiers were trained and compared: Logistic Regression, Decision Tree and Random Forest. Logistic Regression was selected as the best-performing model and serves the stream.",
        "Predictions are persisted in MongoDB and displayed in an interactive Streamlit dashboard of traffic conditions across Paris."],
 results=[],
 gallery=[("paris/dashboard","Streamlit dashboard","Dashboard"),("paris/architecture","Pipeline architecture","Architecture"),("paris/models","Model comparison","Model comparison")])

add(slug="hadoop-sales", title="Sales Analysis with Hadoop MapReduce",
 short="Analysis of more than 4 million sales transactions with Hadoop MapReduce and Python through Hadoop Streaming.",
 cats=["bigdata"], stack=["Hadoop","MapReduce","Python","Hadoop Streaming"],
 cover="hadoop/categories", cover_fit="contain", repo=GH+"hadoop-mapreduce-sales-analysis", detail=False)

add(slug="sportlinebot", title="SportLineBot: Field-Marking Robot",
 short="Autonomous sports-field line-marking robot on an ESP32-S3, controlled from a Flask dashboard with French NLP commands and ML anomaly detection.",
 cats=["embedded","nlp","ml"], stack=["ESP32-S3","Arduino","Flask","Socket.IO","scikit-learn"],
 cover="sportlinebot/dashboard", cover_fit="cover", repo=GH+"sportlinebot-field-marking-robot", detail=True,
 context="MECA WORLD CUP 2026, with Abdelaaziz Ait Kheri",
 problem="Marking the lines of a sports field by hand is slow and imprecise. SportLineBot drives and sprays paint on its own while an operator supervises from a browser, with buttons or by typing a sentence in French such as \"trace un terrain de foot\".",
 built=["Firmware for an ESP32-S3 with a WebSocket server, time-based motion, an ultrasonic sensor on a servo for obstacle scanning, a paint pump and a paint-level sensor.",
        "Flask and Socket.IO dashboard with a live field view that follows the 7 steps of a football field (outer rectangle, halfway line, centre circle and both penalty and goal areas).",
        "An NLP intent classifier (TF-IDF character n-grams and Multinomial Naive Bayes, 8 intents, about 130 French phrases) that turns a sentence into a robot command.",
        "Anomaly monitoring with safety rules first (paint empty, obstacle closer than 15 cm, low paint) and an Isolation Forest second.",
        "A mock ESP32 so the dashboard can be tested without the robot."],
 results=["Hackathon prototype at reduced scale; only the football field is implemented and the motion is open loop, so it must be calibrated.",
          "The team received a certificate of participation at the MECA WORLD CUP, organised by the Club Mécatronique of ENSA Tétouan."],
 gallery=[("sportlinebot/dashboard","SportLineBot dashboard","Dashboard"),("sportlinebot/robot","SportLineBot prototype","Prototype")])

add(slug="heart-guardian", title="Heart Guardian: ECG-Driven Adaptive Game",
 short="A wearable ESP32 ECG sensor streams the heart signal; XGBoost classifies the rhythm and a Unity game adapts in real time.",
 cats=["embedded","ml"], stack=["ESP32","XGBoost","Pan-Tompkins","Python","Unity","SQLite"],
 cover="heartguardian/prototype", cover_fit="cover", repo=GH+"heart-guardian-ecg-game", detail=True,
 context="Game4Health Hackathon 2026, team Health Hackers",
 problem="Diabetes and obesity are rising in Morocco. Heart Guardian builds cardiac monitoring into a game so that physical activity is motivating and heart-rate anomalies are caught early.",
 built=["An ESP32 samples a 3-electrode ECG sensor at 100 Hz and streams it over WiFi.",
        "A Python pipeline detects R peaks with a Pan-Tompkins style algorithm and computes heart rate, HRV and rhythm irregularity.",
        "An XGBoost classifier trained on 10-second segments from the MIT-BIH Arrhythmia Database labels the rhythm (normal, bradycardia, tachycardia, danger); thresholds adapt to the player's age and condition.",
        "A Unity game receives one JSON result per second and adapts (normal pace, slow down, breathing pause, safe mode). Sessions, results and alerts are stored in SQLite.",
        "An ECG emulator and a Unity simulator let the project run without hardware."],
 results=["Hackathon prototype built with a business model and cost study; estimated MVP cost 2,400 to 3,500 MAD.",
          "Not a medical device: labels come from heart-rate and irregularity rules, and the system has not been clinically validated."],
 gallery=[("heartguardian/prototype","Prototype: ESP32 and ECG electrodes","Prototype"),("heartguardian/architecture","System architecture","Architecture"),("heartguardian/solution","Solution overview","Solution")])

add(slug="university-dwh-bi", title="University Data Warehouse and BI",
 short="End-to-end Business Intelligence: star-schema data warehouse, SSIS ETL pipelines, SSAS OLAP cube and Power BI dashboards.",
 cats=["bi"], stack=["SQL Server","SSIS","SSAS","Power BI","T-SQL"],
 cover="dwbi/dashboard", cover_fit="cover", repo=GH+"University-Data-Warehouse-BI-Project", detail=False)

add(slug="power-bi-hr", title="HR Analytics Dashboard",
 short="Interactive Power BI dashboard on workforce, promotions, retrenchments and satisfaction.",
 cats=["bi"], stack=["Power BI"], cover="powerbi/overview", cover_fit="cover", repo=GH+"power-bi-hr-dashboard", detail=False)

add(slug="tableau-science", title="Global Scientific Production Dashboard",
 short="Interactive Tableau dashboard on world scientific production, 1996-2014: documents, citations, H-index and country rankings.",
 cats=["bi"], stack=["Tableau","Tableau Public"], cover="tableau/countries", cover_fit="cover", repo=GH+"tableau-global-scientific-production", demo="https://public.tableau.com/app/profile/abdessamad.ait.brahim/viz/Histoire1-Analysedelaproductionscientifique/Analysedelaproductionscientifique", detail=False)

add(slug="yelp-n8n", title="Web Scraping: Yelp and n8n",
 short="Automated Python and Selenium scraping for Yelp data analysis, plus an n8n workflow for multi-source smartphone price tracking.",
 cats=["bi","bigdata"], stack=["Python","Selenium","n8n","Docker"], cover="yelp/workflow", cover_fit="cover", repo=GH+"web-scraping-yelp-n8n", detail=False)

add(slug="numerical-linear-algebra", title="Numerical Linear Algebra in Python",
 short="Linear systems (LU, Cholesky, Jacobi, Gauss-Seidel), SVD, QR and PCA with NumPy and SciPy, including image compression.",
 cats=["foundations"], stack=["Python","NumPy","SciPy","Jupyter"], cover=None, label="Linear algebra", repo=GH+"numerical-linear-algebra-python", detail=False)

add(slug="cryptography", title="Symmetric and Asymmetric Cryptography",
 short="Study of AES, RSA, Diffie-Hellman and ElGamal for the Security and Cryptography course (December 2025), with a report and mind maps.",
 cats=["foundations"], stack=["AES","RSA","Diffie-Hellman","ElGamal"], cover="crypto/aes", cover_fit="contain", repo=GH+"cryptography-symmetric-asymmetric-analysis", detail=False)

add(slug="dsa-cpp", title="C++ Data Structures and Algorithms",
 short="Data structures and algorithms implemented from scratch in C++17: pointers, OOP, sorting, recursion, stacks, queues, linked lists and dynamic programming.",
 cats=["foundations"], stack=["C++"], cover=None, label="C++ DSA", repo=GH+"dsa-cpp-practice", detail=False)

S = json.load(open("img_sizes.json"))
for p in P:
    p["gallery"] = [dict(img=g[0], alt=g[1], caption=g[2], w=S[g[0]][0], h=S[g[0]][1]) for g in p.get("gallery", [])]
    if p.get("cover"): p["cover_w"], p["cover_h"] = S[p["cover"]]
    p.setdefault("results", [])

SITE = dict(
 name="Abdessamad Ait Brahim",
 url="https://abdessamadaitbrahim.github.io",
 github="https://github.com/abdessamadaitbrahim",
 linkedin="https://www.linkedin.com/in/abdessamad-aitbrahim/",
 email_user="abdessamadaitbrahim9", email_domain="gmail.com",
)
json.dump(dict(site=SITE, projects=P), open("content.json","w"), ensure_ascii=False, indent=1)
print(len(P), "projects;", sum(1 for p in P if p["detail"]), "detail pages")
