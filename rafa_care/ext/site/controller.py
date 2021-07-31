import sqlalchemy.exc
from flask import Blueprint, redirect, render_template, request, session, url_for, \
    current_app, jsonify

from rafa_care.ext.dao import BreastfeedingDao, MilkSourceDao
from rafa_care.ext.dao import MedicationDao
from rafa_care.ext.dao.medicine_dao import MedicineDao
from rafa_care.ext.models import Breastfeeding, Medication, Medicine

bp = Blueprint("site", __name__)

@bp.get("/")
def home():
    breastfeedings = BreastfeedingDao.get_all()
    return render_template("index.html", breastfeedings=breastfeedings)


@bp.get("/mamando")
def new_breastfeeding():
    breastfeeding_id = session.get("breastfeeding_id")
    if not breastfeeding_id:
        breastfeeding = Breastfeeding.start()
        breastfeeding.save()
        session["breastfeeding_id"] = breastfeeding.id
    else:
        breastfeeding = BreastfeedingDao.get_by_id(breastfeeding_id)
        if breastfeeding is None:
            session.pop("breastfeeding_id")

    milk_sources = MilkSourceDao.get_all()
    return render_template(
        "breastfeeding.html", milk_sources=milk_sources, breastfeeding=breastfeeding
    )


@bp.post("/encerra_mama")
def finish_breastfeeding():
    data = request.form

    breastfeeding_id = data.get("id")
    breastfeeding = BreastfeedingDao.get_by_id(breastfeeding_id)

    breastfeeding.finish(
        milk_source_id=data.get("milk_sources"),
        started_at=data.get("started_at"),
        note=data.get("note"),
    )

    session.pop("breastfeeding_id")

    return redirect(url_for("site.home"))


@bp.get("/mama/editar/<int:id_>")
def edit_breastfeeding(id_):
    milk_sources = MilkSourceDao.get_all()
    breastfeeding = BreastfeedingDao.get_by_id(id_)
    session.pop("breastfeeding_id")
    return render_template(
        "breastfeeding_edit.html",
        milk_sources=milk_sources,
        breastfeeding=breastfeeding,
    )


@bp.post("/atualiza_mama")
def update_breastfeeding():
    data = request.form

    breastfeeding_id = data.get("id")
    breastfeeding = BreastfeedingDao.get_by_id(breastfeeding_id)

    breastfeeding.update(
        milk_source_id=data.get("milk_sources"),
        started_at=data.get("started_at"),
        finished_at=data.get("finished_at"),
        note=data.get("note"),
    )

    return redirect(url_for("site.home"))


@bp.get("/remedios")
def medication_list():
    medications = MedicationDao.get_all()
    return render_template("medications.html", medications=medications)


@bp.get("/dar_remedio")
def give_medicine():
    medicines = MedicineDao.get_all()
    return render_template("medication_edit.html", medication=None, medicines=medicines)


@bp.get("/atualiza_remedio/<int:medication_id>")
def update_medication(medication_id):
    medication = MedicationDao.get_by_id(medication_id)
    medicines = MedicineDao.get_all()
    return render_template(
        "medication_edit.html",
        medication=medication,
        medicines=medicines
    )


@bp.post("/salva_remedio")
def save_medication():
    data = request.form
    medication_id = data.get("id")
    if medication_id:
        medication = MedicationDao.get_by_id(medication_id)
    else:
        medication = Medication()
    medication.medicine_id = int(data.get("medicine"))
    medication.gave_at = data.get("gave_at")
    medication.note = data.get("note") or None
    medication.save()

    return redirect(url_for("site.medication_list"))


@bp.post("/new_medicine")
def new_medicine():
    data = request.get_json(True)
    medicine_name = data.get("name").upper()
    try:
        medicine = Medicine(name=medicine_name, dosage=data.get("dosage"))
        medicine.save()
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"error": "Medicine already exists"})

    return jsonify({"medicine_id": medicine.id, "name": str(medicine)})
