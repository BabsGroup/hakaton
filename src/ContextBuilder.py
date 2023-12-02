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
    select * FROM (
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
    ) AS u
    ORDER BY u.distance
    """
def p_build_query(coordinates, diff, where):
    la = coordinates.latitude
    lo = coordinates.longitude

    la1 = la - diff
    la2 = la + diff

    lo1 = lo - diff
    lo2 = lo + diff

    where = ' AND '.join(where)

    return f"""
    SELECT * FROM (
        SELECT 
            osm_id, 
            name,
            amenity,
            ST_Distance(
                ST_centroid(way), 
                ST_GeomFromText(
                    'SRID=4326;POINT({lo} {la})'
                )
            ) AS distance
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
            amenity,
            ST_Distance(
                ST_centroid(way), 
                ST_GeomFromText(
                    'SRID=4326;POINT({lo} {la})'
                )
            ) AS distance
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
            amenity,
            ST_Distance(
                ST_centroid(way), 
                ST_GeomFromText(
                    'SRID=4326;POINT({lo} {la})'
                )
            ) AS distance
        FROM planet_osm_line
        WHERE ST_Intersects(
            way,
            ST_GeomFromText(
                'SRID=4326;POLYGON(({lo1} {la1}, {lo1} {la2}, {lo2} {la2}, {lo2} {la1}, {lo1} {la1}))'
            )
        ) {where}
        
    ) as u 
    ORDER BY u.distance
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

    def get_text_context(self, coordinates, text, keys):
        city = 'Город Москва.'

        metro_context = self.find_nearest_metro_station(coordinates)
        current_place_context = self.find_current_place(coordinates, keys)
        current_address_context = self.find_current_address(coordinates)

        context = f"{metro_context} {current_place_context} {current_address_context} {city}"
        tips = self.build_tips(text, context)

        return f"{context} {tips}"

    def find_nearest_metro_station(self, coordinates):
        sql = p_build_query(coordinates, 0.1, [
            'AND 1=1',
            'name IS NOT NULL',
            "railway='station'"
        ])

        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        if len(result) > 0:
            metro_name = result[0][1]
            return f"Ближайшая станция метро: {metro_name}."

        return ''

    def find_current_place(self, coordinates, keys):
        where = ['AND 1=1', 'name IS NOT NULL']
        diff = 0.005

        if len(keys.type) == 0:
            return ''

        type = ''
        if keys.type == 'парк':
            type = 'парк'
            where.append("leisure='park'")

        if keys.type == 'здание' or keys.type == 'дом':
            type = 'здание'
            where.append("(building IS NOT NULL OR amenity IS NOT NULL)")

        if keys.type == 'памятник':
            type = 'памятник'
            where.append("historic='memorial'")

        sql = p_build_query(coordinates, diff, where)

        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()

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

            return f"Примерное место: {type} {name}."

        return ''

    def find_current_address(self, coordinates):
        street_query = p_build_street_query(coordinates)
        cur = self.conn.cursor()
        cur.execute(street_query)
        street_result = cur.fetchall()

        street = ''
        if len(street_result) > 0:
            street = street_result[0][1]

        boundary_query = p_build_query(coordinates, 0.005, [
            'AND 1=1',
            'name IS NOT NULL',
            "boundary='administrative'",
            "admin_level='8'"
        ])

        cur = self.conn.cursor()
        cur.execute(boundary_query)
        boundary_result = cur.fetchall()

        boundary = ''
        if len(boundary_result) > 0:
            print(boundary_result)
            boundary = boundary_result[0][1]

        if len(street) != 0 or len(boundary) != 0:
            return f"Текущее местоположение: {boundary}, {street}."

        return ''

    def build_tips(self, text, context):
        tips = ''
        if 'андре' in text.lower() and 'смирно' in text.lower():
            tips += 'Андрей Смирнов - backend разработчик в компании профи. Он любит путешествовать и ему скоро 21 годик.'

        if ('орловск' in text.lower() and 'сад' in text.lower()) or ('орловск' in context.lower() and 'сад' in context.lower()):
            tips += """
Орловский Сад - Скамейки: да. Описание: парк находится на некоторой возвышенности, поднимающейся холмом как раз к центру двора, к спортивной площадке.
Около трех десятков деревьев в парке явно имеют возраст более 100-150 лет; остальные, видимо, высажены при массовом жилищном строительстве в районе Коровинского и Дмитровского шоссе в 1960-е гг."""

        if len(tips) == 0:
            return ''
        else:
            return f"""Подсказки: {tips}
По возможности пиши что-нибудь от себя"""
