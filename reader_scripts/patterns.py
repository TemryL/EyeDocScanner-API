name = r"([a-zA-z][a-zA-z\- ]*[a-zA-z])"
date = r"([0-3]\d[\./][0-1]\d[\./]\d{4})"
time = r"(\d{2}:\d{2}(?::\d{2})?)"
date_time = f"{date} {time}"
angle = r"(\d{1,3}) °"

shape_sphere = r"([+-]? ?[1-3]?\d\.(?:00|25|50|75))"
shape_cylinder = shape_sphere
shape_axis = angle
shape_alcon = f"{shape_sphere} D {shape_cylinder} D x {shape_axis}"
shape_sophtalmo = rf"{shape_sphere} \( ?{shape_cylinder} à {shape_axis}\)"

add = r"([0-4]\.(?:00|25|50|75))"

acuity_far_main = (
    r"(?:\d\.\d{1,2}|FC|CLD|CD|CF|HM|VBLM|VM|MM|(?:LP|PL)[\+\-]?)"
)
acuity_far_sub = r"(?:3/5|4/5|5/5|f|ff|\+|-|--|p|pp|faible)"
acuity_far = rf"({acuity_far_main}(?: \({acuity_far_sub}\))?)"

acuity_near = r"(P\d{1,2}(?:\.\d)?f)"
IOP = r"([(?:APL)(?:\d{1,2}(?:\.\d))]+)"

kerato_mm = r"(\d\.\d{2})"
kerato_as = r"(\d{1,3})"
kerato_dio = r"(\d{1,2}\.(?:00|25|50|75))"
kerato_javal = r"([+-]\d\.(?:00|25|50|75))"

length_mm = r"(\d+\.\d{2}) mm"
length_um = r"(\d{1,4}) [up]m"
time_s = r"(\d{1,3}) [sS]"

K = r"(\d+\.\d{2}) D"
K_axis = angle
Q = r"([+-]?\d+\.\d{2}|-+)"
KQ = f"{K} @ {K_axis} / {Q}"
