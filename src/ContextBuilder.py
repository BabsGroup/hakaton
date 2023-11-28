import psycopg2

def p_build_street_query(coordinates):
    la = coordinates.latitude
    lo = coordinates.longitude

    diff = 0.005
    la1 = la - diff
    la2 = la + diff

    lo1 = lo - diff
    lo2 = lo + diff

    return f"""
    SELECT 
        osm_id, 
        name,
        "addr:housename" AS housename,
        "addr:housenumber" AS housenumber,
        ST_Distance(
            ST_centroid(way), 
            ST_GeomFromText(
                'SRID=4326;POINT({lo} {la})'
            )
        ) AS distance
    FROM planet_osm_roads
    WHERE ST_Intersects(
        way,
        ST_GeomFromText(
            'SRID=4326;POLYGON(({lo1} {la1}, {lo1} {la2}, {lo2} {la2}, {lo2} {la1}, {lo1} {la1}))'
        )
    ) 
        AND highway IS NOT NULL 
        AND name IS NOT NULL
    """
def p_build_query(coordinates, where):
    la = coordinates.latitude
    lo = coordinates.longitude

    diff = 0.005
    la1 = la - diff
    la2 = la + diff

    lo1 = lo - diff
    lo2 = lo + diff

    where = ' AND '.join(where)

    return f"""
        SELECT 
            osm_id, 
            name,
            amenity
        FROM planet_osm_point 
        WHERE ST_Intersects(
            way,
            ST_GeomFromText(
                'SRID=4326;POLYGON(({lo1} {la1}, {lo1} {la2}, {lo2} {la2}, {lo2} {la1}, {lo1} {la1}))'
            )
        ) {where}
    UNION
        SELECT 
            osm_id, 
            name,
            amenity
        FROM planet_osm_polygon
        WHERE ST_Intersects(
            way,
            ST_GeomFromText(
                'SRID=4326;POLYGON(({lo1} {la1}, {lo1} {la2}, {lo2} {la2}, {lo2} {la1}, {lo1} {la1}))'
            )
        ) {where}
    UNION 
        SELECT 
            osm_id, 
            name,
            amenity
        FROM planet_osm_line
        WHERE ST_Intersects(
            way,
            ST_GeomFromText(
                'SRID=4326;POLYGON(({lo1} {la1}, {lo1} {la2}, {lo2} {la2}, {lo2} {la1}, {lo1} {la1}))'
            )
        ) {where}
    """

class ContextBuilder:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="moscow",
            user="postgres",
            password="verySecret",
            host="localhost",
            port="5432"
        )

    def get_text_context(self, coordinates, keys):
        where = ['AND 1=1', 'name IS NOT NULL']

        type = 'объект'
        if keys.type == 'парк':
            type = 'парк'
            where.append("leisure='park'")

        if keys.type == 'строение':
            type = 'строение'
            where.append("(building IS NOT NULL OR amenity IS NOT NULL)")

        if keys.type == 'памятник':
            type = 'памятник'
            where.append("historic='memorial'")

        query = p_build_query(coordinates, where)
        street_query = p_build_street_query(coordinates)

        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchall()

        name = ''
        if len(result) > 0:
            print(result[0])
            name = result[0][1]

            amenity = result[0][2]
            amenity_map = {
                'cinema': 'кинотеатр',
                'library': 'библиотека',
                'school': 'школа',
                'university': 'университет',
                'fountain': 'фонтан',
                'theatre': 'театр'
            }

            if amenity in amenity_map:
                type = amenity_map[amenity]

        cur = self.conn.cursor()
        cur.execute(street_query)
        street_result = cur.fetchall()

        street = ''
        if len(street_result) > 0:
            street = f', расположенный на {street_result[0][1]}'

        return f"{type} {name}{street} в городе Москва"
