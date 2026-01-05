import os

def calculate_ipk(grades):
    """
    Calculate IPK (Indeks Prestasi Kumulatif) based on the given grades.

    Rules:
    - IPK = Σ(SKS × Nilai Angka) / Σ(SKS)
    - Only include courses with passing grades (nilai ≥ D, i.e., numeric ≥ 1)
    - For repeated courses, take the highest grade
    - If no passing grades, return 0.0

    Args:
        grades (list): List of dicts with keys 'kode', 'nama', 'sks', 'nilai'

    Returns:
        float: Calculated IPK
    """
    if not grades:
        return 0.0

    # Grade to numeric mapping
    grade_to_numeric = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}

    # Group by kode to handle repeats, take highest grade
    course_best_grades = {}
    for grade in grades:
        kode = grade['kode']
        nilai = grade['nilai']
        sks = grade['sks']
        numeric = grade_to_numeric.get(nilai, 0)
        if kode not in course_best_grades or numeric > course_best_grades[kode]['numeric']:
            course_best_grades[kode] = {'sks': sks, 'numeric': numeric, 'nilai': nilai}

    # Calculate IPK only for passing grades (numeric >= 1)
    total_mutu = 0.0
    total_sks = 0
    for course in course_best_grades.values():
        if course['numeric'] >= 1:  # Passing grade
            total_mutu += course['sks'] * course['numeric']
            total_sks += course['sks']

    if total_sks == 0:
        return 0.0

    return round(total_mutu / total_sks, 2)

def get_predikat(ipk):
    """Get predikat based on IPK"""
    if ipk >= 3.5:
        return "Cum Laude"
    elif ipk >= 3.0:
        return "Sangat Memuaskan"
    elif ipk >= 2.5:
        return "Memuaskan"
    elif ipk >= 2.0:
        return "Cukup"
    else:
        return "Kurang"

def generate_transcript_pdf(student_data, output_path):
    """
    Generate transcript PDF using ReportLab

    Args:
        student_data (dict): Student data including biodata and grades
        output_path (str): Path to save the PDF
    """
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
    except ImportError:
        print("Error: ReportLab is not available. Cannot generate PDF.")
        return

    # Prepare data for PDF
    all_grades = []
    for semester in student_data['semesters']:
        all_grades.extend(semester['grades'])

    total_sks = sum(grade['sks'] for grade in all_grades if grade['nilai'] != 'E')
    ipk = calculate_ipk(all_grades)
    predikat = get_predikat(ipk)

    # Create PDF document
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("TRANSKRIP AKADEMIK", title_style))
    story.append(Spacer(1, 12))

    # University header
    story.append(Paragraph("Universitas Indonesia", styles['Heading2']))
    story.append(Spacer(1, 20))

    # Student info
    info_data = [
        ['NIM', ':', student_data['nim']],
        ['Nama', ':', student_data['nama']],
        ['Program Studi', ':', student_data['program_studi']],
        ['Angkatan', ':', str(student_data['angkatan'])]
    ]

    info_table = Table(info_data, colWidths=[100, 20, 200])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 20))

    # Grades by semester
    for semester in student_data['semesters']:
        semester_title = ParagraphStyle(
            'SemesterTitle',
            parent=styles['Heading3'],
            fontSize=12,
            spaceAfter=10
        )
        story.append(Paragraph(f"Semester {semester['nomor']}", semester_title))

        # Table header
        grade_data = [['Kode MK', 'Nama MK', 'SKS', 'Nilai', 'Mutu']]

        # Add grade rows
        grade_to_numeric = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
        for grade in semester['grades']:
            mutu = grade['sks'] * grade_to_numeric.get(grade['nilai'], 0)
            grade_data.append([
                grade['kode'],
                grade['nama'],
                str(grade['sks']),
                grade['nilai'],
                str(mutu)
            ])

        # Create table
        grade_table = Table(grade_data, colWidths=[60, 150, 30, 40, 40])
        grade_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(grade_table)
        story.append(Spacer(1, 15))

    # Summary section
    summary_data = [
        ['Total SKS', ':', str(total_sks)],
        ['IPK', ':', f"{ipk:.2f}"],
        ['Predikat', ':', predikat]
    ]

    summary_table = Table(summary_data, colWidths=[80, 20, 150])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 30))

    # Signature
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1
    )
    story.append(Paragraph("Dekan Fakultas", signature_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("(___________________________)", signature_style))
    story.append(Paragraph("Dr. John Doe", signature_style))

    # Build PDF
    doc.build(story)
    print(f"Transcript PDF generated: {output_path}")
