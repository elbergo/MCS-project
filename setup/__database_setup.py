import sqlite3
from sqlite3 import Error


def create_tables():
    conn = None
    try:
        conn = sqlite3.connect('deviceservice.db')

        # Create cumulocity table
        conn.execute("""
            CREATE TABLE Cumulocity (
                Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                Username NVARCHAR NOT NULL,
                TenantId NVARCHAR NOT NULL,
                Password NVARCHAR NOT NULL,
                Active BIT NOT NULL
            )
        """)        

        # Create Device table
        conn.execute("""
            CREATE TABLE Device (
                Id uuid PRIMARY KEY NOT NULL,
                Name NVARCHAR NOT NULL,
                Color NVARCHAR NOT NULL,
                Brand NVARCHAR NOT NULL,
                Password NVARCHAR NOT NULL,
                CumulocityId INTEGER NULL,

                CONSTRAINT fk_Device_Cumulocity
                    FOREIGN KEY(CumulocityId) 
                    REFERENCES Cumulocity(Id)
                    ON DELETE CASCADE
            )
        """)

        # Create GPS logger table
        conn.execute("""
            CREATE TABLE Position (
                Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                DeviceId uuid NOT NULL,
                Latitude DECIMAL NOT NULL,
                Longitude DECIMAL NOT NULL,
                Altitude DECIMAL NOT NULL,
                CreatedDateTime timestamp NOT NULL,

                CONSTRAINT fk_Position_Device
                    FOREIGN KEY(DeviceId) 
                    REFERENCES Device(Id)
                    ON DELETE CASCADE
            )
        """)

        # Create EmergencyContact table
        conn.execute("""
            CREATE TABLE EmergencyContact (
                Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                DeviceId NVARCHAR NOT NULL,
                Name NVARCHAR NOT NULL,
                PhoneNumber NVARCHAR NOT NULL,
                
                CONSTRAINT fk_EmergencyContact_Device
                    FOREIGN KEY(DeviceId)
                    REFERENCES Device(Id)
                    ON DELETE CASCADE
            )
        """)

        conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def populate():
    conn = None
    try:
        conn = sqlite3.connect('deviceservice.db')

        conn.execute('PRAGMA foreign_keys = ON')

        conn.execute("INSERT INTO Cumulocity VALUES (NULL, 'Hello', 'hello', 'Password123', 0)")

        conn.execute("""
            INSERT INTO Device
                VALUES
                    ('6cc4cf69-843d-407b-9d03-2b70b2efe9c5', 'Motorcykeln', 'Blue', 'Yamaha', 'Äpple123', NULL),
                    ('64ef1aad-adc0-4a15-9e02-e752f837a0fe', 'Cykeln', 'Gray', 'Honda', 'Gurka123', NULL),
                    ('5d634db7-be28-4bce-986a-6426c502428e', 'Mopeden', 'Yellow', 'KTM', 'Päron123', NULL),
                    ('cb8e0fef-62f0-4c74-8b5e-70abe923feeb', 'Teslan', 'Green', 'Tesla', 'Kaffe123', 1),
                    ('3e76f96f-5bd1-49e6-85d6-8d34cb124924', 'Båten', 'White', 'Fjord', 'Tårta123', NULL),
                    ('af849430-0f28-4e03-b20e-470a62266302', 'Tjänstebilen', 'Svart', 'Volvo', 'Anannas123', NULL),
                    ('680ebc91-4f96-4388-98f5-8a180b4b00c7', 'Fritidsbilen', 'Silver', 'Shelby GT 500', 'Kiwi123', NULL)
        """)

        conn.execute("""
            INSERT INTO EmergencyContact
                VALUES
                    (NULL, '6cc4cf69-843d-407b-9d03-2b70b2efe9c5', 'Johan', '+46XXXXXXXX0'),
                    (NULL, '64ef1aad-adc0-4a15-9e02-e752f837a0fe', 'Andreas', '+46XXXXXXXX1'),
                    (NULL, '5d634db7-be28-4bce-986a-6426c502428e', 'Jessica', '+46XXXXXXXX2'),
                    (NULL, 'cb8e0fef-62f0-4c74-8b5e-70abe923feeb', 'Jesper', '+46XXXXXXXX3'),
                    (NULL, 'cb8e0fef-62f0-4c74-8b5e-70abe923feeb', 'Johan', '+46XXXXXXXX4'),
                    (NULL, '3e76f96f-5bd1-49e6-85d6-8d34cb124924', 'Andreas', '+46XXXXXXXX5'),
                    (NULL, 'af849430-0f28-4e03-b20e-470a62266302', 'Jessica', '+46XXXXXXXX6'),
                    (NULL, 'af849430-0f28-4e03-b20e-470a62266302', 'Jesper', '+46XXXXXXXX7'),
                    (NULL, 'af849430-0f28-4e03-b20e-470a62266302', 'Johan', '+46XXXXXXXX8'),
                    (NULL, 'af849430-0f28-4e03-b20e-470a62266302', 'Andreas', '+46XXXXXXXX9'),
                    (NULL, '680ebc91-4f96-4388-98f5-8a180b4b00c7', 'Jessica', '+46XXXXXXX10')
        """)

        conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def main():
    create_tables()
    populate()


if __name__ == '__main__':
    main()
