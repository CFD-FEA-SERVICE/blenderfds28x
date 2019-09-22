import bpy, logging
from bpy.app.handlers import persistent, load_post, save_pre, depsgraph_update_post
from bpy.types import Object

from .. import geometry
from .. import config

log = logging.getLogger(__name__)

# Handlers


@persistent
def _load_post(self):  # Beware: self is None
    # Check file format version FIXME
    # check_file_version(context)
    # Init FDS default materials
    for k, v in config.default_mas.items():
        if not bpy.data.materials.get(k):  # check existance
            ma = bpy.data.materials.new(k)
            ma.bf_export = True
            ma.diffuse_color = v[0]
            ma.use_fake_user = True
    # if not fds.surf.has_predefined(): bpy.ops.material.bf_set_predefined()
    # Set default scene appearance
    # for scene in bpy.data.scenes: scene.set_default_appearance(context=None)


@persistent
def _save_pre(self):  # Beware: self is None
    geometry.utils.rm_tmp_objects(bpy.context)
    # Set file format version
    # set_file_version(bpy.context) FIXME


@persistent
# def _depsgraph_update_post(scene):
#     # Detect object change and erase cached geometry
#     for update in bpy.context.view_layer.depsgraph.updates:
#         ob = update.id.original
#         if (
#             isinstance(ob, Object)
#             and ob.type in {"MESH", "CURVE", "SURFACE", "FONT", "META"}
#             and (update.is_updated_geometry or update.is_updated_transform)
#         ):
#             ob["ob_to_geom_cache"] = False
#             ob["ob_to_xbs_cache"] = False
#             ob["ob_to_xyzs_cache"] = False
#             ob["ob_to_pbs_cache"] = False


# Register


def register():
    log.debug(f"Registering handlers")
    load_post.append(_load_post)
    save_pre.append(_save_pre)


#    depsgraph_update_post.append(_depsgraph_update_post)


def unregister():
    log.debug(f"Unregistering handlers")
    load_post.remove(_load_post)
    save_pre.remove(_save_pre)


#    depsgraph_update_post.remove(_depsgraph_update_post)
