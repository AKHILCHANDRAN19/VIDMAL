from shapely.geometry import Polygon
import skia


class GeometryBooleans:

    @staticmethod
    def polygon_to_skia_path(poly: Polygon) -> skia.Path:
        path = skia.Path()
        coords = list(poly.exterior.coords)
        if not coords:
            return path
        path.moveTo(coords[0][0], coords[0][1])
        for pt in coords[1:]:
            path.lineTo(pt[0], pt[1])
        path.close()
        return path

    @staticmethod
    def union_to_skia(poly_a_pts: list, poly_b_pts: list) -> skia.Path:
        pa = Polygon(poly_a_pts)
        pb = Polygon(poly_b_pts)
        res = pa.union(pb)
        return GeometryBooleans.polygon_to_skia_path(res)

    @staticmethod
    def difference_to_skia(poly_a_pts: list, poly_b_pts: list) -> skia.Path:
        pa = Polygon(poly_a_pts)
        pb = Polygon(poly_b_pts)
        res = pa.difference(pb)
        return GeometryBooleans.polygon_to_skia_path(res)

    @staticmethod
    def buffer_polygon_to_skia(pts: list, distance: float) -> skia.Path:
        p = Polygon(pts)
        buffered = p.buffer(distance, join_style="round")
        return GeometryBooleans.polygon_to_skia_path(buffered)
