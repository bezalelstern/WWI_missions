
CREATE INDEX idx_mission_year ON mission (date_part('year', mission_date));
SELECT
    mission.air_force,
    mission.target_city,
    COUNT(*) AS mission_count
FROM
    mission
WHERE
    date_part('year' , mission_date) = 1943
GROUP BY
    mission.air_force, mission.target_city
ORDER BY
    mission_count DESC
LIMIT 1;


CREATE INDEX idx_airborne_aircraft ON mission (airborne_aircraft);

SELECT
    mission.target_country,
    max(bomb_damage_assessment) AS damage
FROM
    mission
WHERE
    mission.airborne_aircraft > 5
GROUP BY
    mission.target_country;