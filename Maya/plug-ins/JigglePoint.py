import  maya.OpenMayaMPx as OpenMayaMPx
import  maya.OpenMaya as OpenMaya
import  math

class JigglePoint(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00001234)

    aOutput = OpenMaya.MObject()
    aGoal = OpenMaya.MObject()
    aDamping = OpenMaya.MObject()
    aStiffness = OpenMaya.MObject()
    aTime = OpenMaya.MObject() # time node
    aParentInverse = OpenMaya.MObject()


    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        self._initialized = False
        self._currentPosition = OpenMaya.MPoint()
        self._previousPosition = OpenMaya.MPoint()
        self._previousTime = OpenMaya.MTime()

    def compute(self, plug, data):
        if plug != JigglePoint.aOutput:
            return OpenMaya.kUnknownParameter

        # Get the inputs
        damping = data.inputValue(self.aDamping).asFloat()
        stiffness = data.inputValue(self.aStiffness).asFloat()
        goal = OpenMaya.MPoint(data.inputValue(self.aGoal).asFloatVector())
        currentTime = data.inputValue(self.aTime).asTime()
        parentInverse = data.inputValue(self.aParentInverse).asMatrix()

        if not self._initialized:
            self._previousTime = currentTime
            self._currentPosition = goal
            self._previousPosition = goal
            self._initialized = True

        # Check if the timestep is just 1 frame since we want a stable simulation
        timeDifference = currentTime.value() - self._previousTime.value()
        if timeDifference > 1.0 or timeDifference <0.0:
            self._initialized = False
            self._previousTime = currentTime
            data.setClean(plug)
            return

        velocity = (self._currentPosition - self._previousPosition) * (1.0-damping)
        newPosition = self._currentPosition + velocity
        goalForce = (goal - newPosition) * stiffness
        newPosition += goalForce

        # Store the states for the next computation
        self._previousPosition = OpenMaya.MPoint(self._currentPosition)
        self._currentPosition = OpenMaya.MPoint(newPosition)
        self._previousTime = OpenMaya.MTime(currentTime )

        # Put in the output local space
        newPosition *= parentInverse

        hOutput = data.outputValue(JigglePoint.aOutput)
        outVector = OpenMaya.MFloatVector(newPosition.x,newPosition.y,newPosition.z)
        hOutput.setMFloatVector(outVector)
        hOutput.setClean()
        data.setClean(plug)


def creator():
    return OpenMayaMPx.asMPxPtr(JigglePoint())

def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    uAttr = OpenMaya.MFnUnitAttribute()
    mAttr = OpenMaya.MFnMatrixAttribute()


    JigglePoint.aOutput = nAttr.createPoint('output', 'out')
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    JigglePoint.addAttribute(JigglePoint.aOutput)

    JigglePoint.aGoal = nAttr.createPoint('goal', 'goal')
    JigglePoint.addAttribute(JigglePoint.aGoal)
    JigglePoint.attributeAffects(JigglePoint.aGoal,JigglePoint.aOutput)

    JigglePoint.aTime = uAttr.create('time', 'time',OpenMaya.MFnUnitAttribute.kTime,0.0)
    JigglePoint.addAttribute(JigglePoint.aTime)
    JigglePoint.attributeAffects(JigglePoint.aTime, JigglePoint.aOutput)

    JigglePoint.aStiffness = nAttr.createPoint('stiffness', 'stiffness')
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    JigglePoint.addAttribute(JigglePoint.aStiffness)
    JigglePoint.attributeAffects(JigglePoint.aStiffness,JigglePoint.aOutput)

    JigglePoint.aDamping = nAttr.createPoint('damping', 'damping',OpenMaya.MFnNumericData.kFloat,1.0)
    nAttr.setKeyable(True)
    nAttr.setMin(0.0)
    nAttr.setMax(1.0)
    JigglePoint.addAttribute(JigglePoint.aDamping)
    JigglePoint.attributeAffects(JigglePoint.aDamping, JigglePoint.aOutput)

    JigglePoint.aParentInverce = mAttr.create("parentInverse","parentInverse")
    JigglePoint.addAttribute(JigglePoint.aParentInverce)

def initializePlugin(obj):
    fnPlugin = OpenMayaMPx.MFnPlugin(obj,"Neozheng","1.0","Any")
    fnPlugin.registerNode("jigglePoint",JigglePoint.kPluginNodeId,creator,initialize)

def uninitializePlugin(obj):
    fnPlugin = OpenMayaMPx.MFnPlugin(obj)
    fnPlugin.deregisterNode(JigglePoint.kPluginNodeId)

