from flask import Blueprint, redirect, render_template, request, session, url_for

from rafa_care.ext.dao import BreastfeedingDao, MilkSourceDao
from rafa_care.ext.models import Breastfeeding

bp = Blueprint("site", __name__)


@bp.get("/")
def home():
    breastfeedings = BreastfeedingDao.get_all()
    return render_template("index.html", breastfeedings=breastfeedings)


@bp.post("/mamando")
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
