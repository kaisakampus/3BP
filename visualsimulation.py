# taken from https://gist.github.com/BrianWeinstein/81df3f7c9a2d7d1d6d9e
Manipulate[
 Show[
  {ParametricPlot3D[
    {
     {x1[t], y1[t], z1[t]},
     {x2[t], y2[t], z2[t]},
     {x3[t], y3[t], z3[t]}
     },
    {t, 1.005, tmax},
    Axes -> False,
    Ticks -> True,
    Boxed -> False,
    PlotRange -> {{-1.25, 0.75}, {0, 3.5}, {-0.5, 4}},
    PlotStyle -> {Lighter[Red, 0.5], Lighter[Green, 0.5], 
      Lighter[Blue, 0.5]},
    FaceGrids -> {{0, 0, -1}, {0, 1, 0}, {-1, 0, 0}}
    ]
   },
  {ParametricPlot3D[
    {
     {x1[t], y1[t], z1[t]},
     {x2[t], y2[t], z2[t]},
     {x3[t], y3[t], z3[t]}
     },
    {t, tmax - 1, tmax},
    PlotStyle -> {{Thick, Red}, {Thick, Green}, {Thick, Blue}}
    ]
   },
  {Graphics3D[
    {Red, Sphere[{x1[tmax], y1[tmax], z1[tmax]}, mA/spScale],
     Green, Sphere[{x2[tmax], y2[tmax], z2[tmax]}, mB/spScale],
     Blue, Sphere[{x3[tmax], y3[tmax], z3[tmax]}, mC/spScale]}
    ]
   },
  ImageSize -> {500, 500}
  ],
 {tmax, 1, 8.8}
 ]