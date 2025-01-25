from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
from ovito.pipeline import *
import sys

# Data import:
#pipeline = import_file(sys.argv[1], multiple_frames = True)
pipeline = import_file("dump.lammpstrj", multiple_frames = True)

# Selection:
pipeline.modifiers.append(ExpressionSelectionModifier(expression = 'ParticleType==1 && Position.Z>42'))

# Compute property:
pipeline.modifiers.append(ConstructSurfaceModifier(method = ConstructSurfaceModifier.Method.AlphaShape,radius = 6.0,only_selected=True,compute_distances=True))

num_frames=pipeline.source.num_frames
#print(num_frames)


for frame in range(1,pipeline.source.num_frames):
    data = pipeline.compute(frame)

export_file(pipeline, "dump.alphashape.xyz", "xyz", columns =["Particle Identifier", "Particle Type", "Surface Distance"],start_frame=0,end_frame=num_frames-1,multiple_frames=True)
