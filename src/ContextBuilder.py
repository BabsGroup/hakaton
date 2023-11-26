import psycopg2

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
        where = ['AND 1=1']

        if keys.type == 'парк':
            where.append("leisure='park'")

        query = self.p_build_query(coordinates, where)
        print(query)


        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return f"Город Москва, Объект {result[0][1]}"


    def p_build_query(self, coordinates, where):
        la = coordinates.latitude
        lo = coordinates.longitude

        diff = 0.01
        la1 = la - 0.01
        la2 = la + 0.01

        lo1 = lo - 0.01
        lo2 = lo + 0.01

        where = ' AND '.join(where)

        return f"""
        SELECT 
            osm_id, 
            name,
            ST_Distance(
                ST_centroid(way), 
                ST_GeomFromText(
                    'SRID=4326;POINT({la} {lo})'
                )
            ) AS distance
        FROM planet_osm_point 
        WHERE ST_Intersects(
            way,
            ST_GeomFromText(
                'SRID=4326;POLYGON(({lo1} {la1}, {lo1} {la2}, {lo2} {la2}, {lo2} {la1}, {lo1} {la1}))'
            )
        ) {where};
        """