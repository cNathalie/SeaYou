use SeaYouDatabase

CREATE TABLE Ship (

    ShipId INT IDENTITY(1, 1),
    ShipName NVARCHAR(100) NOT NULL,
    IMO INT NOT NULL,
	Max_Length DECIMAL(8,2) NOT NULL,
	Max_Width DECIMAL(8,2) NOT NULL,
	Max_Draft DECIMAL(8,2) NOT NULL,
	OperationalDraft DECIMAL(8,2),
	
	CONSTRAINT PK_ShipId PRIMARY KEY (ShipId),
	CONSTRAINT CHK_Ship_IMO CHECK (IMO BETWEEN 1000000 AND 9999999),
    CONSTRAINT UQ_Ship_NameIMO UNIQUE (ShipName,IMO)
);

CREATE TABLE RouteCategory (

	RouteCategoryId INT IDENTITY(1,1),
	RouteCategoryName NVARCHAR(50) NOT NULL,
	
	CONSTRAINT PK_RouteCategory PRIMARY KEY (RouteCategoryId),
	CONSTRAINT UQ_RouteCategory_Name UNIQUE (RouteCategoryName)
);

CREATE TABLE ZoneTo (

	ZoneToId INT IDENTITY(1,1),
	ZoneToName NVARCHAR(50) NOT NULL,
	
	CONSTRAINT PK_ZoneTo PRIMARY KEY (ZoneToId),
	CONSTRAINT UQ_ZoneTo_Name UNIQUE (ZoneToName)	

);

-- Waypoint = Locatie (excel) = Passagepunt
CREATE TABLE Waypoint(  
	
	WaypointId INT IDENTITY(1,1),
	WaypointName VARCHAR(10) NOT NULL,
	WaypointDescription VARCHAR(max),
	WaypointLongitude VARCHAR(max),
	WaypointLatitude VARCHAR(max),
	
	CONSTRAINT PK_WaypointId PRIMARY KEY (WaypointId ),
	CONSTRAINT UQ_Waypoint_Name UNIQUE (WaypointName)	
);

-- Visit = Verblijf (excel), Journey = Reis
CREATE TABLE Route(
	
	RouteId INT IDENTITY(1,1),
	Visit VARCHAR(7) NOT NULL,
	Journey INT NOT NULL,
	ShipId INT NOT NULL,
	RouteCategoryId INT NOT NULL,
	RouteStartedDT DATETIME NOT NULL,
	WaypointId INT NOT NULL,
	WaypointDT DATETIME NOT NULL,
	DockedDT DATETIME, 
	ZoneToId int NOT NULL,
	
	CONSTRAINT PK_RouteID PRIMARY KEY (RouteId),
	CONSTRAINT FK_Route_ShipId FOREIGN KEY (ShipId) REFERENCES Ship(ShipId),
	CONSTRAINT FK_Route_RouteCategoryId FOREIGN KEY (RouteCategoryId) REFERENCES RouteCategory(RouteCategoryId),
	CONSTRAINT FK_Route_WaypointId FOREIGN KEY (WaypointId) REFERENCES Waypoint(WaypointId),
	CONSTRAINT FK_Route_ZoneToId FOREIGN KEY (ZoneToId) REFERENCES ZoneTo(ZoneToId)
);