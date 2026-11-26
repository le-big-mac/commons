"""Print the TIFF and GeoTIFF tags of the first page of each file given (no pixel is read).
usage: python -I tags.py FILE.tif ..."""
import sys
import tifffile

for path in sys.argv[1:]:
    print('=====', path)
    with tifffile.TiffFile(path) as t:
        print('pages', len(t.pages), 'is_bigtiff', t.is_bigtiff, 'byteorder', t.byteorder)
        p = t.pages[0]
        print('shape', p.shape, 'dtype', p.dtype, 'compression', p.compression, 'predictor', p.predictor,
              'tiled', p.is_tiled, 'tile', getattr(p, 'tilewidth', None), getattr(p, 'tilelength', None),
              'rowsperstrip', getattr(p, 'rowsperstrip', None), 'photometric', p.photometric,
              'planarconfig', p.planarconfig, 'samplesperpixel', p.samplesperpixel, 'sampleformat', p.sampleformat)
        for tag in p.tags.values():
            v = tag.value
            s = repr(v)
            if len(s) > 400:
                s = s[:400] + ' ...'
            print('  tag', tag.code, tag.name, tag.dtype, tag.count, s)
        try:
            print('  geotiff_tags', p.geotiff_tags)
        except Exception as ex:
            print('  geotiff_tags failed', ex)
        # overviews / sub-IFDs
        for i, q in enumerate(t.pages[1:6], 1):
            print('  page', i, q.shape, q.dtype)
