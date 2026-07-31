# Qualification attempt log (fields)

Machine template: `data/operations/qualification_attempt_log_template.csv`

Required fields per attempt:

- coded_id  
- attempt_number  
- qualification_set_id  
- package_checksum  
- release_timestamp_utc  
- submission_timestamp_utc  
- technical_incident (yes/no)  
- answer_key_exposure (yes/no)  
- attempt_validity (valid / invalid_technical / invalid_exposure)  
- scoring_record_path (private)  
- pass_fail (pass / fail / not_scored)  
- reviewer_id  
- decision_timestamp_utc  
- next_action (retry_other_set / fail_final / activate_ready_checklist)
