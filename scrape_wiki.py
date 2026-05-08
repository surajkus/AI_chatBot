import wikipediaapi
import concurrent.futures
import os

# Create folder
os.makedirs("data", exist_ok=True)

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='MyScraper/1.0 (aman-chatbot-project-fast)'
)

topics = [
    # ---------- AI / ML ----------
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Neural Networks",
    "Computer Vision",
    "Natural Language Processing",
    "Generative AI",
    "Reinforcement Learning",
    "Robotics",
    "Supervised Learning",
    "Unsupervised Learning",
    "Semi-supervised learning",
    "Neural architecture search",
    "Large Language Model",
    "ChatGPT",
    "Transformer (machine learning model)",
    "Support Vector Machine",
    "Decision Tree",
    "Random Forest",
    "Gradient Boosting",
    "K-means clustering",
    "Convolutional Neural Network",
    "Recurrent Neural Network",
    "LSTM",
    "Autoencoder",
    "GAN (Generative adversarial network)",
    "Markov Decision Process",
    "Computer Vision",
    "Sentiment analysis",

    # ---------- Programming ----------
    "Python (programming language)",
    "Java (programming language)",
    "C++",
    "C (programming language)",
    "JavaScript",
    "React (web framework)",
    "Node.js",
    "HTML",
    "CSS",
    "TypeScript",
    "PHP",
    "SQL",
    "NoSQL",
    "MongoDB",
    "MySQL",
    "PostgreSQL",
    "Django",
    "Flask",
    "Laravel",
    "Spring Framework",
    "Android (operating system)",
    "iOS",
    "Kotlin",
    "Swift",
    "Docker",
    "Kubernetes",
    "Cloud computing",
    "Distributed computing",

    # ---------- Computer Science ----------
    "Computer Science",
    "Operating System",
    "Computer Network",
    "Database",
    "Software Engineering",
    "Algorithm",
    "Data Structure",
    "Compiler",
    "Cybersecurity",
    "Cloud computing",
    "Virtualization",
    "Microprocessor",
    "Quantum computing",
    "Information theory",

    # ---------- Physics ----------
    "Physics",
    "Classical mechanics",
    "Quantum mechanics",
    "Thermodynamics",
    "Electricity",
    "Magnetism",
    "Electromagnetic radiation",
    "Nuclear physics",
    "Particle physics",
    "String theory",
    "Relativity",
    "Einstein",

    # ---------- Chemistry ----------
    "Chemistry",
    "Organic chemistry",
    "Inorganic chemistry",
    "Physical chemistry",
    "Periodic table",
    "Chemical reaction",
    "Polymers",
    "Biochemistry",

    # ---------- Biology ----------
    "Biology",
    "Human brain",
    "Human body",
    "Genetics",
    "DNA",
    "RNA",
    "Evolution",
    "Microbiology",
    "Cell biology",
    "Neuroscience",
    "Immunology",
    "Physiology",

    # ---------- Mathematics ----------
    "Mathematics",
    "Algebra",
    "Calculus",
    "Geometry",
    "Statistics",
    "Probability",
    "Trigonometry",
    "Differential equations",
    "Linear algebra",
    "Number theory",
    "Discrete mathematics",
    "Set theory",
    "Game theory",

    # ---------- History ----------
    "World War 1",
    "World War 2",
    "French Revolution",
    "Industrial Revolution",
    "American Revolution",
    "Cold War",
    "Roman Empire",
    "Greek civilization",
    "Egyptian civilization",
    "Indian independence movement",
    "Mughal Empire",
    "British Empire",
    "Russian Revolution",

    # ---------- Geography ----------
    "India",
    "United States",
    "China",
    "Russia",
    "Japan",
    "Brazil",
    "Germany",
    "France",
    "United Kingdom",
    "Canada",
    "Australia",
    "Africa",
    "Asia",
    "Europe",
    "South America",
    "North America",

    # ---------- Economics ----------
    "Economics",
    "Macroeconomics",
    "Microeconomics",
    "Inflation",
    "GDP",
    "Stock market",
    "Finance",
    "Cryptocurrency",
    "Bitcoin",
    "Blockchain",

    # ---------- Psychology ----------
    "Psychology",
    "Human behavior",
    "Mental health",
    "Personality psychology",
    "Social psychology",
    "Cognitive psychology",
    "Learning theory",

    # ---------- Technology ----------
    "Internet",
    "Cyber security",
    "Artificial neural network",
    "Smartphone",
    "Mobile computing",
    "Web development",
    "Software testing",
    "Information security",
    "Data Science",
    "Big Data",
    "Internet of Things",
    "5G",
    "Augmented Reality",
    "Virtual Reality",

    # ---------- Astronomy ----------
    "Universe",
    "Solar System",
    "Milky Way",
    "Black hole",
    "Big Bang",
    "Galaxy",
    "Star",
    "Planet",
    "Space exploration",
    "NASA",
    "ISRO",

    # ---------- Famous Scientists ----------
    "Albert Einstein",
    "Isaac Newton",
    "Nikola Tesla",
    "Stephen Hawking",
    "Marie Curie",
    "Charles Darwin",
    "Richard Feynman",

    # ---------- Famous Inventors ----------
    "Thomas Edison",
    "Alexander Graham Bell",
    "Elon Musk",
    "Steve Jobs",
    "Bill Gates",

    # ---------- Misc General Knowledge ----------
    "Climate change",
    "Global warming",
    "Renewable energy",
    "Education",
    "Economy of India",
    "Health",
    "Medicine",
    "Vaccination",
    "Artificial organs",
    "Food science",
    "Environment",
    "Sustainable development",
]


def fetch_and_save(topic):
    try:
        page = wiki.page(topic)
        if not page.exists():
            return f"❌ Not found: {topic}"

        filename = f"data/{topic.replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(page.text)

        return f"✔ Saved: {topic}"
    except Exception as e:
        return f"⚠ Error {topic}: {e}"


print("🚀 Starting FAST Wikipedia scraping...")

# Use 30 threads (5600H can handle it easily)
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    results = executor.map(fetch_and_save, topics)

for r in results:
    print(r)

print("\n🎉 All topics scraped successfully!")
