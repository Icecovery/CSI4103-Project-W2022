float sizeMult = 1.5; // size multiplier to make stuff easier to see

PVector pageSize = new PVector(216, 279);
PVector originPoint = new PVector(200, 100); // origin point of the paper

PVector jointA = PVector.add(originPoint, new PVector(-50, pageSize.y/2)); // origin point of the arm
PVector jointB = new PVector(100, 100);
PVector target = new PVector(200, 200);
float La = 160; // length of arm a
float Lb = 150; // length of arm b

float angleA; // angle of the frist joint
float angleB; // angle of the second joint

float smallestA = Float.POSITIVE_INFINITY;
float smallestB = Float.POSITIVE_INFINITY;

ArrayList<PVector> points = new ArrayList<PVector>();

void setup()
{
  size(800, 800);
}

void draw()
{
  background(0);
  scale(sizeMult);
  
  // handle mouse press event
  if (mousePressed)
  {
    if (mouseButton == LEFT) // draw
    {
      // make sure it is in range
      if (mouseX / sizeMult > originPoint.x && mouseX / sizeMult < originPoint.x + pageSize.x && mouseY / sizeMult > originPoint.y &&  mouseY / sizeMult < originPoint.y + pageSize.y)
      {
          points.add(new PVector(mouseX / sizeMult, mouseY / sizeMult));
      }
    }
    else if (mouseButton == RIGHT) // clear
    {
      points = new ArrayList<PVector>();
    }
  }
  
  // get target position
  target = new PVector(clamp(mouseX / sizeMult, originPoint.x, originPoint.x + pageSize.x), 
                       clamp(mouseY / sizeMult, originPoint.y, originPoint.y + pageSize.y));
  
  float AC = PVector.dist(jointA, target);
  float BAC = acos((sq(La) + sq(AC) - sq(Lb))/(2.0 * La * AC));
  float YAC = asin((target.x - jointA.x) / AC);
  float YAB = (target.y < jointA.y) ? (PI - YAC - BAC) : (YAC - BAC);
  
  // position is reletive to A
  float Bx = sin(YAB) * La;
  float By = sin(HALF_PI - YAB) * La;
  
  jointB = new PVector(Bx, By).add(jointA);
  
  // drawing
  drawPage();
  drawPath();
  drawArm();
  
  angleA = degrees(YAB);
  angleB = degrees(acos((sq(La) + sq(Lb) - sq(AC))/(2.0 * La * Lb)));
  
  smallestA = min(angleA, smallestA);
  smallestB = min(angleB, smallestB);
  
  println("A " + angleA + " B " + angleB + " A min " + smallestA + " B min " + smallestB);
}

void drawPage()
{
  noStroke();
  rect(originPoint.x, originPoint.y, pageSize.x, pageSize.y);
}

void drawPath()
{
  strokeWeight(2);
  stroke(0, 0, 0);
  for (int i = 0; i < points.size(); i++)
  {
    PVector p = points.get(i);
    point(p.x, p.y);
  }
}

void drawArm()
{
  strokeWeight(5);
  
  stroke(100, 100, 100);
  line(jointA.x, jointA.y, jointB.x, jointB.y);
  line(target.x, target.y, jointB.x, jointB.y);
  
  strokeWeight(10);
  
  stroke(255, 0, 0);
  point(jointA.x, jointA.y);
  
  stroke(0, 255, 255);
  point(jointB.x, jointB.y);
  
  stroke(0, 255, 0);
  point(target.x, target.y);
  
}

float clamp(float v, float min, float max)
{
  return min(max(v, min), max);
}
