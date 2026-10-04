import re

# Skills commonly encountered in software/AI/data/networking resumes.
SKILLS = {
    "python", "java", "c", "c++", "c#", "scala", "r", "sql",
    "mysql", "postgresql", "mongodb", "oracle",
    "html", "css", "javascript", "typescript", "react", "angular",
    "node.js", "nodejs", "express", "django", "flask", "fastapi",
    "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow",
    "pytorch", "keras", "opencv", "streamlit",
    "machine learning", "deep learning", "artificial intelligence",
    "natural language processing", "nlp", "computer vision",
    "data science", "data analytics", "data visualization",
    "power bi", "tableau", "excel",
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
    "git", "github", "linux", "rest api", "api",
    "fastapi", "spring", "spring boot",
    "spark", "hadoop", "kafka",
    "xgboost", "random forest", "resnet", "densenet", "efficientnet",
    "vgg16", "yolo", "shap", "explainable ai",
    "cyber security", "networking", "network security",
    "operating systems", "dbms", "data structures", "dsa"
}


def extract_skills(text):
    text = text.lower()
    found = set()

    # Longer/multi-word skills first.
    for skill in sorted(SKILLS, key=len, reverse=True):
        pattern = r"(?<![a-z0-9+#.-])" + re.escape(skill.lower()) + r"(?![a-z0-9+#.-])"
        if re.search(pattern, text):
            found.add(skill)

    # Normalize a few common aliases.
    if "sklearn" in found:
        found.add("scikit-learn")
    if "nodejs" in found:
        found.add("node.js")

    return sorted(found)
