-- ============================================================
-- 1. Number of trials by study type and phase
-- ============================================================
SELECT study_type, phase,
       COUNT(*) AS total_trials
  FROM clinical_trials.studies
 GROUP BY study_type, phase
 ORDER BY total_trials DESC, study_type, phase;


-- ============================================================
-- 2. Most common conditions being studied
-- ============================================================
SELECT c.condition_name,
       COUNT(DISTINCT sc.nct_id) AS total_trials
  FROM clinical_trials.study_conditions AS sc
       INNER JOIN clinical_trials.conditions AS c
          ON sc.condition_id = c.condition_id
 GROUP BY c.condition_id, c.condition_name
 ORDER BY total_trials DESC, c.condition_name
 LIMIT 20;


-- ============================================================
-- 3. Interventions with the highest completion rates
-- ============================================================
-- A minimum number of trials is required to avoid considering
-- interventions with a 100% completion rate based on only one study.
WITH intervention_completion AS (
    SELECT i.intervention_id, i.intervention_name, i.intervention_type,
        COUNT(DISTINCT si.nct_id) AS total_trials,
        COUNT(DISTINCT si.nct_id) FILTER (
            WHERE s.overall_status = 'COMPLETED'
        ) AS completed_trials
      FROM clinical_trials.study_interventions AS si
          INNER JOIN clinical_trials.interventions AS i
             ON si.intervention_id = i.intervention_id
          INNER JOIN clinical_trials.studies AS s
             ON si.nct_id = s.nct_id
     GROUP BY i.intervention_id, i.intervention_name,i.intervention_type
)

SELECT intervention_name, intervention_type, total_trials, completed_trials,
    ROUND(100.0 * completed_trials / NULLIF(total_trials, 0), 2) AS completion_rate_pct
  FROM intervention_completion
 WHERE total_trials >= 5
 ORDER BY completion_rate_pct DESC, total_trials DESC, intervention_name
 LIMIT 20;


-- ============================================================
-- 4. Geographic distribution of clinical trials
-- ============================================================
-- Count distinct trials instead of locations to avoid inflating
-- countries where the same trial has multiple facilities.
SELECT country,
       COUNT(DISTINCT nct_id) AS total_trials,
       COUNT(*) AS total_locations
  FROM clinical_trials.locations
 WHERE country IS NOT NULL
 GROUP BY country
 ORDER BY total_trials DESC, total_locations DESC, country;


-- ============================================================
-- 5. Timeline analysis of study durations
-- ============================================================

SELECT COUNT(*) AS trials_with_complete_dates,
       ROUND(AVG(completion_date - start_date), 2) AS average_duration_days,
       MIN(completion_date - start_date) AS minimum_duration_days,
       MAX(completion_date - start_date) AS maximum_duration_days
  FROM clinical_trials.studies
 WHERE start_date IS NOT NULL
   AND completion_date IS NOT NULL
   AND completion_date >= start_date;