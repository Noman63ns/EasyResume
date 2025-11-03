from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os, json

app = Flask(__name__)

# Config
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home → template cards
@app.route('/')
def index():
    return render_template("templates_gallery.html")

# Form + Resume Generator
@app.route('/form/<template_name>', methods=['GET', 'POST'])
def form(template_name):
    if request.method == "POST":
        # ----- Personal Info -----
        container1_color = request.form.get("container1_color", "#2c3e50")
        header_color = request.form.get("header_color", "teal")
        name = request.form.get("name")
        designation = request.form.get("designation")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        nationality = request.form.get("nationality")
        profile = request.form.get("profile")
        font_size = request.form.get("fontSize")

        # ----- Photo -----
        photo = request.files.get('photo')
        photo_path = None
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            photo.save(save_path)
            photo_path = f'uploads/{filename}'

        # ----- Helper to split lists -----
        def split_list(field):
            raw = request.form.get(field)
            return [s.strip() for s in raw.split("||")] if raw else []

        # ----- Sections -----
        skills = split_list("skills")
        hobbies = split_list("hobbies")
        language = split_list("language")
        internship_raw = request.form.get("internship")
        internship = []
        if internship_raw:
            intern = [e.strip() for e in internship_raw.split("||") if e.strip()]
            for d in intern:
                parts = [p.strip() for p in d.split("|")]
                if len(parts) == 2:
                    internship.append({
                        "internInput": parts[0],
                        "internTitle": parts[1],
                    })
        extra = split_list("extra")
        research_raw = request.form.get("research")
        research= []
        if research_raw:
            resear = [e.strip() for e in research_raw.split("||") if e.strip()]
            for d in resear:
                parts = [p.strip() for p in d.split("|")]
                if len(parts) == 2:
                    research.append({
                        "researchInput": parts[0],
                        "researchTitle": parts[1],
                    })
        quality = split_list("quality")
        achievement_raw = request.form.get("achievement")
        achievement= []
        if achievement_raw:
            achieve = [e.strip() for e in achievement_raw.split("||") if e.strip()]
            for d in achieve:
                parts = [p.strip() for p in d.split("|")]
                if len(parts) == 2:
                    achievement.append({
                        "achieveInput": parts[0],
                        "achieveTitle": parts[1],
                    })
        courses_raw = request.form.get("courses")
        courses= []
        if courses_raw:
            cour = [e.strip() for e in courses_raw.split("||") if e.strip()]
            for d in cour:
                parts = [p.strip() for p in d.split("|")]
                if len(parts) == 2:
                    courses.append({
                        "courInput": parts[0],
                        "courTitle": parts[1],
                    })

        # ----- Employment -----
        employment_raw = request.form.get("employment")
        employment = []
        if employment_raw:
            jobs = [e.strip() for e in employment_raw.split("||") if e.strip()]
            for j in jobs:
                parts = [p.strip() for p in j.split("|")]
                if len(parts) == 3:
                    job_name, position, date = parts
                    employment.append({"jobName": job_name, "position": position, "date": date})

        # ----- Education -----
        education_raw = request.form.get("education")
        education = []
        if education_raw:
            degrees = [e.strip() for e in education_raw.split("||") if e.strip()]
            for d in degrees:
                parts = [p.strip() for p in d.split("|")]
                if len(parts) == 5:
                    education.append({
                        "degreeName": parts[0],
                        "dateedu": parts[1],
                        "instituteName": parts[2],
                        "department": parts[3],
                        "result": parts[4]
                    })

        # ----- Custom Section -----
        custom_raw = request.form.get("custom")
        custom = []
        if custom_raw:
            try:
                custom = json.loads(custom_raw)
            except:
                custom = []

        # ----- Social Links -----
        facebook = request.form.get("facebook")
        linkedin = request.form.get("linkedin")
        github = request.form.get("github")

        # ----- Render Resume -----
        return render_template(
            f"{template_name}.html",
            name=name,
            designation=designation,
            email=email,
            phone=phone,
            address=address,
            dob=dob,
            gender=gender,
            nationality=nationality,
            profile=profile,
            photo_path=photo_path,
            skills=skills,
            hobbies=hobbies,
            language=language,
            internship=internship,
            extra=extra,
            research=research,
            quality=quality,
            achievement=achievement,
            employment=employment,
            education=education,
            courses=courses,
            custom=custom,
            facebook=facebook,
            linkedin=linkedin,
            github=github,
            font_size=font_size,
            container1_color=container1_color,
            header_color=header_color
        )

    # GET → show form
    return render_template("form.html", template_name=template_name)

if __name__ == '__main__':
    app.run(debug=True)
