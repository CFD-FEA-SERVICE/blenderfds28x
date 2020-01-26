"""!
BlenderFDS, geometric utilities.
"""

import bpy, bmesh

from ..types import BFException


# Working on Blender objects


def get_object_bmesh(context, ob, matrix=None, world=False, triangulate=False, lookup=False) -> "BMesh":
    """!
    Return evaluated object bmesh.
    @param context: the <a href="https://docs.blender.org/api/current/bpy.context.html">blender context</a>.
    @param ob: the Blender object.
    @param matrix: ???
    @param world: ???
    @param triangulate: ???
    @param lookup: ???
    @return the evaluated bmesh.
    """
    print("#########################################")
    print("#########################################")
    print(type(matrix))
    print("#########################################")
    print("#########################################")
    # Check object and init
    if ob.type not in {"MESH", "CURVE", "SURFACE", "FONT", "META"}:
        raise BFException(ob, "Object cannnot be converted into mesh")
    # if context.object:
    #    bpy.ops.object.mode_set(mode="OBJECT")  # actualize FIXME not allowed in panel calls
    # Get evaluated bmesh from ob
    bm = bmesh.new()
    depsgraph = context.evaluated_depsgraph_get()
    bm.from_object(ob, depsgraph=depsgraph, deform=True, cage=False, face_normals=True)
    if matrix is not None:
        bm.transform(matrix)  # transform
    if world:
        bm.transform(ob.matrix_world)  # set in world coordinates
    if triangulate:  # triangulate faces
        bmesh.ops.triangulate(bm, faces=bm.faces)
    if lookup:  # update bm indexes for reference
        bm.faces.ensure_lookup_table()
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
    return bm


def get_tmp_object(context, ob, name="tmp"):
    """!
    Get a new tmp Object from ob.
    @param context: the <a href="https://docs.blender.org/api/current/bpy.context.html">blender context</a>.
    @param ob: the Blender object.
    @param name: the new object name.
    @return the temp object.
    """
    # Create new tmp Object
    co_tmp = context.collection
    me_tmp = bpy.data.meshes.new(name)
    ob_tmp = bpy.data.objects.new(name, me_tmp)
    ob_tmp.bf_is_tmp = True
    co_tmp.objects.link(ob_tmp)
    # Set original
    ob.bf_has_tmp = True
    ob.hide_set(True)
    return ob_tmp


def rm_tmp_objects(context):
    """!
    ???
    @param context: the <a href="https://docs.blender.org/api/current/bpy.context.html">blender context</a>.
    """
    mes = bpy.data.meshes
    for ob in context.scene.objects:
        if ob.bf_is_tmp:
            mes.remove(
                ob.data, do_unlink=True
            )  # best way to remove an Object wo mem leaks
        elif ob.bf_has_tmp:
            ob.bf_has_tmp = False
            ob.hide_set(False)
            ob.select_set(True)


# Working on Blender materials


def get_new_material(context, name) -> "Material":
    """!
    Create new material, named name.
    @param context: the <a href="https://docs.blender.org/api/current/bpy.context.html">blender context</a>.
    @param name: the new material name.
    @return the new material.
    """
    return bpy.data.materials.new(name)


def get_material_by_name(context, name) -> "Material or None":
    """!
    Get a material by name and return it.
    @param context: the <a href="https://docs.blender.org/api/current/bpy.context.html">blender context</a>.
    @param name: the material name.
    @return the material if exist. None otherwise.
    """
    if name and name in bpy.data.materials:
        return bpy.data.materials[name]


def get_material(context, name) -> "Material or None":
    """!
    Get an existing material by name or create a new one, and return it.
    @param context: the <a href="https://docs.blender.org/api/current/bpy.context.html">blender context</a>.
    @param name: the material name.
    @return the material.
    """
    if name and name in bpy.data.materials:
        return bpy.data.materials[name]
    return bpy.data.materials.new(name)


# Working on bounding box and size


def get_bbox_xbs(context, ob, scale_length, world=False) -> "x0, x1, y0, y1, z0, z1":
    """!
    Get object’s bounding box in xbs format.
    @param context: the <a href="https://docs.blender.org/api/current/bpy.context.html">blender context</a>.
    @param ob: the Blender object.
    @param scale_length: the scale to use.
    @param world: ???
    @return the object’s bounding box.
    """
    if world:
        bm = get_object_bmesh(context, ob, world=True)
        bm.verts.ensure_lookup_table()
        if not bm.verts:
            raise BFException(ob, "No exported geometry!")
        xs, ys, zs = tuple(zip(*(v.co for v in bm.verts)))
        bm.free()
        return (
            min(xs) * scale_length,
            max(xs) * scale_length,
            min(ys) * scale_length,
            max(ys) * scale_length,
            min(zs) * scale_length,
            max(zs) * scale_length,
        )
    else:
        bb = ob.bound_box  # needs updated view_layer
        return (
            bb[0][0] * scale_length,
            bb[6][0] * scale_length,
            bb[0][1] * scale_length,
            bb[6][1] * scale_length,
            bb[0][2] * scale_length,
            bb[6][2] * scale_length,
        )

