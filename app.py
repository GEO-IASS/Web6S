from flask import Flask, send_file, render_template, redirect, url_for, request, session
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import *
from StringIO import StringIO
from Py6S import *

app = Flask(__name__)

@app.route('/image')
def image():
  return render_template('image.html')

@app.route('/py6sparams', methods=["POST", "GET"])
def params():
  aot = float(request.form['aot'])
  return run(aot)

@app.route('/py6s/<aot>')
def run(aot):
  s = SixS()
  s.altitudes.set_target_sea_level()
  s.altitudes.set_sensor_satellite_level()
  s.ground_reflectance = GroundReflectance.HomogeneousLambertian(GroundReflectance.GreenVegetation)
  s.aot550 = float(aot)
  results = SixSHelpers.Wavelengths.run_vnir(s, spacing=0.1, output_name="apparent_radiance")

  xs = ",".join(map(str, list(results[0])))
  ys = ",".join(map(str, list(results[1])))

  return redirect(url_for('show', x=xs, y=ys, params="none", lab="AOT = %.2f" % s.aot550))

@app.route('/show/<x>/<y>')
@app.route('/show/<x>/<y>/<params>')
@app.route('/show/<x>/<y>/<params>/<lab>')
def show(x, y, params = "", lab=""):
  if params == "clear":
    clf()
  xvals = map(float, x.split(','))
  yvals = map(float, y.split(','))

  print "Label is:"
  print lab

  plot(xvals, yvals, label=lab)
  legend()

  xlabel("Wavelength ($\mu m$)")
  ylabel("Radiance ($W/m^2/sr$)")

  img = StringIO()
  savefig(img)
  img.seek(0)
  #return send_file(img, mimetype='image/png')
  return img.getvalue().encode("base64").strip()

@app.route('/clear')
def clear():
  clf()

if __name__ == '__main__':
  app.run(debug = True)
