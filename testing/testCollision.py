import sys
import blessed
import random
import math

term = blessed.Terminal()

sys.path.append(__file__[:-24] + "sandsea/")
import objects
accuracies = 0
inaccuracies = 0
while True:
    print(term.white_on_black("Beginning new collision test ... | "), end="")
    r = random.randint(1, 9)
    xs = random.randint(1, 9)
    ys = random.randint(1, 9)
    zs = random.randint(1, 9)
    sphere = objects.Sphere(objects.Point(xs, ys, zs), r)
    xp = random.randint(1, 9)
    yp = random.randint(1, 9)
    zp = random.randint(1, 9)
    point = objects.Point(xp, yp, zp)
    print(term.lime_on_black("Testing terms successfully generated.") + term.white_on_black(" | "), end="")
    print(term.white_on_black("r=" + str(r) + " xs=" + str(xs) + " ys=" + str(ys) + "zs=" + str(zs) + " xp=" + str(xp) + " yp=" + str(yp) + " zp=" + str(zp) + " | "), end="")
    print(term.yellow_on_black("Checking collision ...") + term.white_on_black(" | "), end="")
    if (sphere.checkCollision(point) and math.sqrt(((xs - xp) ** 2) + ((ys - yp) ** 2) + ((zs - zp) ** 2)) <= r) or ((not sphere.checkCollision(point)) and math.sqrt(((xs - xp) ** 2) + ((ys - yp) ** 2) + ((zs - zp) ** 2)) > r):
        accuracies += 1
        print(term.lime_on_black("Correct.") + term.white_on_black("   | Efficacy: " + str(round(accuracies / (accuracies + inaccuracies), 3) * 100)) + "%")
    else:
        inaccuracies += 1
        print(term.red_on_black("Incorrect.") + term.white_on_black(" | Efficacy: " + str(round(accuracies / (accuracies + inaccuracies), 3) * 100)) + "%")
