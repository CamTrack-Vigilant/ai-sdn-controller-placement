# Synchronized Codebase Context Index (`ai-sdn-controller-placement`)

- **Repository**: `https://github.com/CamTrack-Vigilant/ai-sdn-controller-placement.git`
- **Active Branch**: `add/metodology-annotated`
- **HEAD Commit**: `cc3ee418016c0cfacabdef52e383505e51683bdc`
- **Total Tracked Files**: `587`
- **Generated At**: `2026-11-07T00:29:29.127615+00:00`

## 1. Tracked File Inventory (with SHA-256 Prefix & Line/Byte Counts)

| Relative Path | Size (Bytes) | Lines | SHA-256 (12-char) |
| :--- | :---: | :---: | :---: |
| `.gitignore` | 4800 | binary | `de85618da338` |
| `.vscode/launch.json` | 489 | 16 | `a0970fcb2400` |
| `DATA_COLLECTION_ANALYSIS_ALIGNMENT_DISCOVERY_LOG.md` | 32494 | 501 | `ef8c96f5ea26` |
| `ETHICS.md` | 7193 | 146 | `e327d7222a20` |
| `LICENSE` | 1074 | binary | `d34553454cfc` |
| `PILOT_RUN_REPORT.md` | 10739 | 283 | `a470d0d8a6da` |
| `PROJECT_STATUS.md` | 14474 | 309 | `3d708e40c57c` |
| `README.md` | 24817 | 447 | `8f130f1315d7` |
| `RESEARCH_LOG.md` | 11921 | 224 | `8f0700920fd3` |
| `RUNNING.md` | 12172 | 291 | `89e2ddf636e5` |
| `SDN_Pareto_3D.png` | 557253 | binary | `e70a8f3749de` |
| `SDN_Pareto_3D_Print.png` | 109204 | binary | `5abbd88afb62` |
| `SYNCHRONIZATION_REPORT.md` | 9992 | 297 | `f2e47ef19100` |
| `algorithms/__init__.py` | 57 | 4 | `3f9269538526` |
| `algorithms/ai/__init__.py` | 216 | 8 | `cfc3815b351f` |
| `algorithms/ai/genetic_algorithm.py` | 5401 | 163 | `075729167eab` |
| `algorithms/ai/reinforcement_learning.py` | 16136 | 420 | `e7de4281705e` |
| `algorithms/baseline/__init__.py` | 290 | 10 | `5d90d4ac9429` |
| `algorithms/baseline/greedy_placement.py` | 1166 | 38 | `80f9d1b8e767` |
| `algorithms/baseline/kmeans_placement.py` | 1458 | 46 | `f85723b21280` |
| `algorithms/baseline/random_placement.py` | 542 | 23 | `90cdaa6886f0` |
| `analyze_rl_logs.py` | 9623 | 265 | `629ddfc671d1` |
| `configs/README.md` | 377 | 16 | `e392635626a6` |
| `configs/experiment_config.json` | 1659 | 64 | `f058acbe61ed` |
| `data/processed/.gitkeep` | 52 | binary | `d3d11936d632` |
| `data/processed/topologies/att-mpls.normalized.json` | 15593 | 741 | `464ade0a4524` |
| `data/processed/topologies/internet2.normalized.json` | 5591 | 315 | `c6a068093e51` |
| `data/raw/.gitkeep` | 46 | binary | `0c0113018c28` |
| `data/raw/topologies/AttMpls.graphml` | 18293 | 523 | `c32c3aeb985e` |
| `data/raw/topologies/Internet2.graphml` | 7036 | 214 | `eac8568cb9d3` |
| `demo/quick_demo.sh` | 409 | 13 | `72cc74f123de` |
| `dissertation/00_front_matter.md` | 9203 | 122 | `6e1cb952c82c` |
| `dissertation/01_chapter_1_introduction.md` | 9040 | 62 | `cd3f086843f4` |
| `dissertation/02_chapter_2_literature_review.md` | 10732 | 97 | `8c931473f645` |
| `dissertation/03_chapter_3_methodology.md` | 20892 | 176 | `86a1b0cf44a9` |
| `dissertation/04_chapter_4_results_and_discussion.md` | 31663 | 263 | `519134ad0ffb` |
| `dissertation/05_chapter_5_conclusion.md` | 7293 | 38 | `f97cddbc97a1` |
| `dissertation/06_references.md` | 3396 | 38 | `a3245fa7b99d` |
| `dissertation/07_appendices.md` | 10086 | 173 | `cd30f44e106a` |
| `dissertation/Honours_Mini_Dissertation_Thabang_Buthelezi.docx` | 3647619 | binary | `faade00152a7` |
| `dissertation/Honours_Mini_Dissertation_Thabang_Buthelezi.md` | 102321 | 978 | `744ea0c2a47a` |
| `dissertation/Honours_Mini_Dissertation_Thabang_Buthelezi.pdf` | 2890081 | binary | `e34f6f99a951` |
| `dissertation/compile_dissertation.py` | 46292 | 991 | `a07110b26a3d` |
| `docs/00_DELIVERY_CONFIRMATION.md` | 10768 | 312 | `598eb35649ea` |
| `docs/BIBLIOGRAPHY_ADDITIONS.md` | 5998 | 157 | `8ae7af5d8f2c` |
| `docs/EXECUTION_SUMMARY.md` | 10876 | 262 | `f1c688679682` |
| `docs/FINAL_SUBMISSION_Thabang_Mhlokoma.pdf` | 121626 | binary | `34b148deca0f` |
| `docs/Honours Mini-Dissertation Template (1).docx` | 90506 | binary | `8492f8e6c964` |
| `docs/MANIFEST.md` | 12372 | 331 | `077f8d90540b` |
| `docs/PARETO_DIAGRAM_SPECIFICATION.md` | 10433 | 212 | `dc4d460f500f` |
| `docs/PATCH_CARDS_QUICK_REFERENCE.md` | 10430 | 258 | `72e2278508e9` |
| `docs/PATCH_CHECKLIST_DETAILED.md` | 12864 | 306 | `4cea500434b7` |
| `docs/PHASE4_MININET_GATE_TEST_GUIDE.md` | 11496 | 334 | `aac5871385e0` |
| `docs/PROGRESS_REPORT.md` | 6560 | 101 | `a9742d69672e` |
| `docs/README_START_HERE.md` | 10074 | 330 | `bd45a24ed9ec` |
| `docs/REFERENCE_MANAGEMENT_WORKFLOW.md` | 12945 | 288 | `d555a201f4bd` |
| `docs/Research Proposal  - PG Studies - Hons.pdf` | 4731896 | binary | `6860af2d6d11` |
| `docs/Research Proposal  - PG Studies - Hons.pdf.bak` | 403489 | binary | `a6cf79766edf` |
| `docs/Research Proposal Template with Contant- PG Studies - Hons.pdf` | 471538 | binary | `a6927fcf1bf7` |
| `docs/Research Proposal Template with Contant- PG Studies - Hons_bibliography_audit.txt` | 898 | 13 | `0a930820db12` |
| `docs/Research Proposal Template with Contant- PG Studies - Hons_link_report.txt` | 909 | 16 | `26f2d1fe588a` |
| `docs/Research Proposal Template with Contant- PG Studies - Hons_linked.pdf` | 540382 | binary | `8d37fa67401e` |
| `docs/Research Proposal Template with Contant- PG Studies - Hons_linked_hardened.pdf` | 567159 | binary | `cb0123b4d8c5` |
| `docs/Research_Proposal_Backup.pdf` | 4731896 | binary | `6860af2d6d11` |
| `docs/Research_Proposal_Before_Section3_Update.pdf` | 1051108 | binary | `b1f42fb8ff44` |
| `docs/Research_Proposal_Final_SUBMISSION.pdf` | 45577 | binary | `f116113e42b8` |
| `docs/Research_Proposal_Hardened_Final.pdf` | 916471 | binary | `b9f86996352f` |
| `docs/Research_Proposal_Methodology_Backup.pdf` | 1056731 | binary | `b4798d95ad32` |
| `docs/SATNAC_RESEARCH_PAPER.docx` | 2353217 | binary | `a2fae95f6ef2` |
| `docs/SATNAC_RESEARCH_PAPER.md` | 40642 | 226 | `09a5dd85292e` |
| `docs/SATNAC_RESEARCH_PAPER.pdf` | 2270487 | binary | `7126e5a10fd5` |
| `docs/SATNAC_RESEARCH_PAPER.tex` | 39836 | 296 | `395321101c2a` |
| `docs/SATNAC_RESEARCH_PAPER_Anonymized.docx` | 2353043 | binary | `731bcb9efacc` |
| `docs/SATNAC_RESEARCH_PAPER_CameraReady.docx` | 2353217 | binary | `a2fae95f6ef2` |
| `docs/SECTION_3_COMPLETION_SUMMARY.md` | 13652 | 264 | `69d05555c0e5` |
| `docs/SECTION_3_HARDENING_REPORT.md` | 10015 | 195 | `875b288d2f0b` |
| `docs/STUDY_DESIGN_METHODOLOGY.md` | 44109 | 1001 | `69c733a9829e` |
| `docs/SUPERVISOR_REVIEW_REQUEST.md` | 5102 | 85 | `1146dfe4ecd4` |
| `docs/Section_11_3_timeline_hardening_report.txt` | 439 | 5 | `1824c83dbba1` |
| `docs/VISUAL_FLOWCHART_REFERENCE.md` | 13571 | 365 | `bb22609dade3` |
| `docs/VISUAL_PATCH_GUIDE.md` | 11477 | 280 | `3048b71df2ee` |
| `docs/WRITING_EXCELLENCE_SUMMARY_20260322.md` | 15947 | 282 | `154dfc2d7b43` |
| `docs/_final_submission_extract.txt` | 52847 | 499 | `d4378c517988` |
| `docs/_proposal_final_extract.txt` | 13226 | 194 | `7dfcb2b65b7d` |
| `docs/_proposal_text_extract.txt` | 44482 | 1021 | `22d6cf5dc2c0` |
| `docs/_tmp_link_test.pdf` | 36938 | binary | `e46f171f9eab` |
| `docs/chat_history/2026-10-17_permanent_chat_history.md` | 119763 | 2098 | `7a1ef384afdd` |
| `docs/chat_history/raw_logs/transcript.jsonl.gz` | 159030 | binary | `1ce91f42ec49` |
| `docs/chat_history/raw_logs/transcript_full.jsonl.gz` | 245281 | binary | `414eadcb3f4c` |
| `docs/diagrams/01_complete_experimental_workflow.mmd` | 5654 | binary | `c02b93be2d8d` |
| `docs/diagrams/01_complete_experimental_workflow.png` | 185247 | binary | `f40291f7db36` |
| `docs/diagrams/01_complete_experimental_workflow.svg` | 193434 | binary | `bfb749b055b6` |
| `docs/diagrams/01_complete_experimental_workflow_browser.svg` | 193518 | binary | `2e8f65e32b31` |
| `docs/diagrams/01_complete_experimental_workflow_labeled.png` | 592760 | binary | `be5ed8d002a3` |
| `docs/diagrams/01_complete_experimental_workflow_labeled_cropped.png` | 592760 | binary | `be5ed8d002a3` |
| `docs/diagrams/01_complete_experimental_workflow_labeled_v2.png` | 375222 | binary | `aceaf46730e0` |
| `docs/diagrams/01_complete_experimental_workflow_noforeign.svg` | 167253 | binary | `fdff45352d06` |
| `docs/diagrams/01_complete_experimental_workflow_plain.html` | 5969 | binary | `23e997340e95` |
| `docs/diagrams/01_complete_experimental_workflow_render.html` | 6385 | binary | `bfa956dfa456` |
| `docs/diagrams/01_complete_experimental_workflow_singleline.html` | 5890 | binary | `248ecfa7cc0c` |
| `docs/diagrams/02_per_trial_measurement_protocol.mmd` | 2000 | binary | `29109746bca7` |
| `docs/diagrams/03_phase4_analysis_pipeline.mmd` | 4361 | binary | `207918a33463` |
| `docs/diagrams/04_factorial_design_matrix.mmd` | 3871 | binary | `6e6ddff1cd45` |
| `docs/diagrams/FLOWCHART_SUMMARY.md` | 9482 | 297 | `0ee6b5665f0a` |
| `docs/diagrams/Gemini_Generated_Image_offmw8offmw8offm (1).png` | 1795135 | binary | `8ab18ad7d4de` |
| `docs/diagrams/Gemini_Generated_Image_offmw8offmw8offm.png` | 2180921 | binary | `8370a4e520a7` |
| `docs/diagrams/HOW_TO_EXPORT_IMAGES.md` | 5662 | 212 | `2aa55a23018c` |
| `docs/diagrams/Metodology.png` | 1620232 | binary | `13f65a495b5e` |
| `docs/diagrams/Metodology_annotated.svg` | 3253 | binary | `38922dac858a` |
| `docs/diagrams/Metodology_legend.txt` | 344 | 5 | `5f0fefcb09b2` |
| `docs/diagrams/README.md` | 8328 | 286 | `e38a790660bd` |
| `docs/draft_proposal_presentation_april_2026.md` | 6537 | 168 | `290ae8f2d9e7` |
| `docs/draft_proposal_presentation_april_2026_10_slide.md` | 3968 | 101 | `74ae01a4300d` |
| `docs/draft_proposal_speaker_script_april_2026.md` | 4664 | 66 | `ac7e1246a528` |
| `docs/ethics/Research Protocol for Honours.docx` | 62323 | binary | `497415b9078c` |
| `docs/ethics/data_retention_schedule.md` | 2865 | 64 | `66721d61ea24` |
| `docs/ethics/dataset_intake_form.md` | 2473 | 83 | `7449e1a9d550` |
| `docs/ethics/de_identification_checklist.md` | 2324 | 67 | `f506bb2125a2` |
| `docs/ethics/participant_consent_template.md` | 1275 | 52 | `346e4f384fe3` |
| `docs/figures/conceptual_framework_section_7_1.png` | 354512 | binary | `8f8b282ac4f7` |
| `docs/figures/decision_framework_flowchart.png` | 270901 | binary | `8f8292deda0d` |
| `docs/figures/factorial_benchmark_table.png` | 377645 | binary | `333b962d2ca2` |
| `docs/figures/mininet_rtt_table.png` | 214584 | binary | `a71caab2da45` |
| `docs/figures/pdf_cover_img-000.png` | 121067 | binary | `ba8a32ab139a` |
| `docs/figures/proposal_methodology_workflow.png` | 1795135 | binary | `8ab18ad7d4de` |
| `docs/figures/system_architecture_diagram.png` | 333721 | binary | `2f433d26ef09` |
| `docs/figures/test_top_crop.png` | 719 | binary | `4503532b2043` |
| `docs/figures/unizulu_crest.png` | 122585 | binary | `95b1a112164b` |
| `docs/figures/unizulu_crest_header.png` | 607 | binary | `8472ec855d00` |
| `docs/figures/unizulu_logo.png` | 474 | binary | `61aa209a056c` |
| `docs/literature_review.md` | 833 | 27 | `adc4bb451a5b` |
| `docs/meeting_slide_pack_20260326.md` | 3521 | 71 | `aef4cd643a17` |
| `docs/project_alignment_handout_prof_mudali_20260326.md` | 3966 | 67 | `b7b40daefce1` |
| `docs/proposal.md` | 63261 | 405 | `c8b813bd5da6` |
| `docs/proposal_presentation_hypothesis_evidence_table_20260322.md` | 5093 | 52 | `03e28933bb83` |
| `docs/render_checks/methodology_page_11.png` | 406633 | binary | `f3d581288d90` |
| `docs/render_checks/methodology_page_12.png` | 406270 | binary | `02eeaed4f167` |
| `docs/render_checks/methodology_page_13.png` | 355535 | binary | `b5058689b085` |
| `docs/render_checks/methodology_page_14.png` | 290474 | binary | `f43824f013cb` |
| `docs/render_checks/page_11.png` | 294041 | binary | `64d7cb332626` |
| `docs/render_checks/page_11_v2.png` | 298373 | binary | `0c2c1d5ca574` |
| `docs/render_checks/page_19.png` | 301118 | binary | `e8996a6f714b` |
| `docs/render_checks/page_3.png` | 304362 | binary | `305f2629a3d0` |
| `docs/render_checks/page_3_v2.png` | 309030 | binary | `49324739ffee` |
| `docs/render_checks/page_4_section3_final.png` | 261812 | binary | `f67295972c66` |
| `docs/render_checks/page_4_section3_updated.png` | 274171 | binary | `6a683eb41ff9` |
| `docs/render_checks/page_6.png` | 251347 | binary | `4a079ef591ef` |
| `docs/submit/.~SDN_Controller_Placement_Multi_Objective_Presentation (1).pptx` | 165 | binary | `fc0ae2a15aca` |
| `docs/submit/.~SDN_Controller_Placement_Multi_Objective_Presentation (5) (1).aligned.pptx` | 165 | binary | `fc0ae2a15aca` |
| `docs/submit/.~SDN_Controller_Placement_Multi_Objective_Presentation (5) (1).bgslide2.aligned.pptx` | 165 | binary | `fc0ae2a15aca` |
| `docs/submit/.~SDN_Controller_Placement_Multi_Objective_Presentation (5) (1).pptx` | 165 | binary | `fc0ae2a15aca` |
| `docs/submit/.~SDN_Controller_Placement_Multi_Objective_Presentation (5) (1).slide2keypoints.pptx` | 165 | binary | `fc0ae2a15aca` |
| `docs/submit/Buthelezi TN.docx` | 15661 | binary | `ba894db297b6` |
| `docs/submit/DOC-20260416-WA0011..pdf` | 113445 | binary | `4e840b183ab7` |
| `docs/submit/Honours Proposal Marking Rubric.pdf` | 58877 | binary | `98a6bf96c46d` |
| `docs/submit/One Pager Samples.pdf` | 94861 | binary | `43a9c64f27e2` |
| `docs/submit/Research Proposal Template with Contant- PG Studies - Hons (1).pdf` | 403181 | binary | `7685cd1d33f5` |
| `docs/submit/Research Proposal Template with Contant- PG Studies - Hons (1)_link_report.txt` | 536 | 16 | `30f746002c4a` |
| `docs/submit/Research Proposal Template with Contant- PG Studies - Hons (1)_linked (6).pdf` | 812238 | binary | `acffb35a1df0` |
| `docs/submit/Research Proposal Template with Contant- PG Studies - Hons (1)_linked (6)_hotlinks.pdf` | 812238 | binary | `974c415f4d0c` |
| `docs/submit/Research Proposal Template with Contant- PG Studies - Hons (1)_linked.pdf` | 453329 | binary | `c17982d14498` |
| `docs/submit/SDN_Controller_Placement_Multi_Objective_Presentation (5) (1).pptx` | 54833 | binary | `bf6fd762368d` |
| `docs/submit/Screenshot 2026-05-23 040032.png` | 778690 | binary | `c1715e37ff62` |
| `docs/submit/ThabangNhlokomaButhelezi_OnePager_DRAFT.pdf` | 3913 | binary | `4087c58f99ab` |
| `docs/submit/document.pdf` | 64024 | binary | `ff7f132bbfcf` |
| `docs/submit/hyperlink_batch_report.txt` | 980 | 17 | `6f3b08fca1f2` |
| `docs/submit/~$thelezi TN.docx` | 162 | binary | `42f3a7687208` |
| `env_check.py` | 1697 | 57 | `e9572009aad5` |
| `evaluation/__init__.py` | 960 | 34 | `5a42b7d22f9f` |
| `evaluation/metrics.py` | 10101 | 283 | `e4c48a21d0d1` |
| `evaluation/pareto.py` | 5958 | 181 | `9188c0aad609` |
| `evaluation/performance_analysis.py` | 7472 | 194 | `ceec93c2adc7` |
| `evaluation/telemetry.py` | 9585 | 292 | `07dbe9790e09` |
| `experiments/__init__.py` | 56 | 4 | `19a811b9ca39` |
| `experiments/experiment_runner.py` | 13686 | 396 | `e99485fb3821` |
| `file.jpe` | 3324 | binary | `829f55cdddd4` |
| `logs/.gitkeep` | 42 | binary | `149ed2677ba2` |
| `logs/rl_training.jsonl` | 182056 | binary | `b2660bc54271` |
| `notes/reliability_analysis.md` | 2910 | 45 | `ed0d53f9b0c4` |
| `page_11_render.png` | 264577 | binary | `4d63a235d57b` |
| `page_3_render.png` | 274940 | binary | `2c664f5825c5` |
| `page_4_render.png` | 234442 | binary | `8666449a1d91` |
| `placements/att-mpls_kmeans_k5.json` | 155 | 13 | `1a6a61449358` |
| `placements/internet2_greedy_k2.json` | 123 | 10 | `4a6cf59306b3` |
| `placements/internet2_kcenter_k3.json` | 135 | 11 | `3dd349b68535` |
| `poster/POSTER_Thabang_Mhlokoma_UNIZULU_2026.pdf` | 3696344 | binary | `c8cf7984c59f` |
| `poster/POSTER_Thabang_Mhlokoma_UNIZULU_2026.png` | 4441320 | binary | `c4e8097eab48` |
| `poster/assets/SDN_Pareto_3D.png` | 557253 | binary | `e70a8f3749de` |
| `poster/assets/decision_framework_flowchart.png` | 356582 | binary | `bef44fcacbd2` |
| `poster/assets/dqn_1000_episodes_convergence.png` | 407269 | binary | `abdb5743b323` |
| `poster/assets/factorial_benchmark_table.png` | 350345 | binary | `c48e6c6cd9b7` |
| `poster/assets/mininet_rtt_table.png` | 149589 | binary | `a9e338655eaa` |
| `poster/assets/proposal_methodology_workflow.png` | 1795135 | binary | `8ab18ad7d4de` |
| `poster/assets/system_architecture_diagram.png` | 333721 | binary | `2f433d26ef09` |
| `poster/assets/unizulu_crest_header.png` | 607 | binary | `8472ec855d00` |
| `poster/generate_poster.py` | 28741 | 902 | `3473add35db9` |
| `poster/index.html` | 3869161 | binary | `4bae79cc5405` |
| `poster/render_poster.py` | 1790 | 60 | `ec8b37611bd5` |
| `references.md` | 11212 | 224 | `cf41ccde1d8b` |
| `requirements.txt` | 675 | 21 | `e28553edf9e4` |
| `research_papers/1-s2.0-S1319157823003968-main.pdf` | 2460673 | binary | `929fbf87f266` |
| `research_papers/1-s2.0-S2590123026006717-main.pdf` | 17934632 | binary | `e4417a98666a` |
| `research_papers/2377677.2377767 (1).pdf` | 2194052 | binary | `2b138867c43b` |
| `research_papers/2377677.2377767.pdf` | 2194052 | binary | `d44ae99fc7c0` |
| `research_papers/AI-Enabled_Dynamic_Load_Balancing_and_Mobility_Management_for_Internet_of_Vehicles_in_SDN_6G_Ne.pdf` | 702200 | binary | `0aa5e6c25912` |
| `research_papers/AI-Enhanced_Routing_Optimization_for_SDN_NFV_Architectures_in_Large-Scale_IoT_Networks.pdf` | 311037 | binary | `c888adda7791` |
| `research_papers/A_Comparative_Analysis_of_SDN_Controller_Placement_Problem_IoT-Specific_Tactics_and_Generalized.pdf` | 461636 | binary | `3d6945bd8ea4` |
| `research_papers/A_Controller_Placement_Algorithm_Based_on_Density_Clustering_in_SDN.pdf` | 614652 | binary | `68e32a25a8ef` |
| `research_papers/A_Hierarchical_K-Means_Algorithm_for_Controller_Placement_in_SDN-Based_WAN_Architecture.pdf` | 166636 | binary | `8a5728365ae5` |
| `research_papers/A_Review_on_AI_Driven_Distributed_SDN_for_Energy_-Efficient_Routing_in_Large_Scale_IoT_Network.pdf` | 514349 | binary | `f4a5d1efc794` |
| `research_papers/An_Effective_Controller_Placement_Algorithm_Based_on_Clustering_in_SDN.pdf` | 527971 | binary | `dbfc7d6fbe8e` |
| `research_papers/An_Energy_Efficient_SDN_Controller_Placement_with_Delay_Constraints.pdf` | 744620 | binary | `ab215682f897` |
| `research_papers/CAPFUL_-_Coherent_Dynamic_Controller_Placement_Method_using_deep_reinforcement_learning_for_SDN.pdf` | 518133 | binary | `b01fe1b76891` |
| `research_papers/Deployment_of_an_SDN-based_UAV_network_Controller_placement_and_tradeoff_between_control_overhe.pdf` | 340846 | binary | `1333f65d86d8` |
| `research_papers/Enhanced_SDN_Controller_Placement_and_Load_Balancing_for_Campus_Network_Optimization.pdf` | 1031450 | binary | `364fcf49b470` |
| `research_papers/Enhancing_Security_and_Performance_in_Software-Defined_Networks_Using_AI-Driven_Automation.pdf` | 295926 | binary | `2ac7fa615d53` |
| `research_papers/GOKA_A_Network_Patition_and_Cluster_Fusion_Algorithm_for_Controller_Placement_Problem_in_SDN.pdf` | 160864 | binary | `384cc925733c` |
| `research_papers/Heuristic_Approaches_to_the_Controller_Placement_Problem_in_Large_Scale_SDN_Networks.pdf` | 1391536 | binary | `dad1d47ec5ef` |
| `research_papers/Intent-Based_Networking_with_QoS-Aware_Routing_in_SDN_using_AHP_based_AI_Prioritization_and_Opt.pdf` | 1862930 | binary | `28f2483fb7a8` |
| `research_papers/Minimizing_Latency_for_Controller_Placement_Problem_in_SDN.pdf` | 587416 | binary | `b710c44b07c3` |
| `research_papers/Optimal_Model_for_Link_Failure_Foresight_Controller_Placement_in_SDN.pdf` | 173881 | binary | `eb2076b02ee6` |
| `research_papers/Optimal_Model_for_the_Controller_Placement_Problem_in_Software_Defined_Networks.pdf` | 244773 | binary | `0a3e558966f6` |
| `research_papers/Optimal_and_Dynamic_SDN_Controller_Placement.pdf` | 637881 | binary | `669a3d4de776` |
| `research_papers/Optimizing_the_controller_placement_problem_in_SDN_with_uncertain_parameters_with_robust_optimi.pdf` | 1650375 | binary | `f50a3f7124e5` |
| `research_papers/README.md` | 1624 | 39 | `148754f413f8` |
| `research_papers/Rule_Placement_and_Switch_Migration-based_Scheme_for_Controller_Load_Balancing_in_SDN.pdf` | 446414 | binary | `6f076711177e` |
| `research_papers/SDN-based Solutions.pdf` | 19427848 | binary | `e808d7cfef4a` |
| `research_papers/SDN_controller_placement_design_For_large_scale_production_network.pdf` | 970835 | binary | `c1177b65f470` |
| `research_papers/The_SDN_controller_placement_problem_for_WAN.pdf` | 410126 | binary | `1bdd1ceb87ae` |
| `research_papers/The_role_of_inter-controller_traffic_in_SDN_controllers_placement.pdf` | 901999 | binary | `bef14122f3bd` |
| `research_papers/computers-11-00111.pdf` | 4579466 | binary | `55aaf3b62aa2` |
| `research_papers/matrices/sota_synthesis_matrix.csv` | 13006 | 11 | `0d736cfa8c2b` |
| `research_papers/notes/1-s2.0-S1319157823003968-main_notes.md` | 3996 | 54 | `9ced1e59f8ad` |
| `research_papers/notes/1-s2.0-S2590123026006717-main_notes.md` | 3855 | 54 | `5506e0f76c44` |
| `research_papers/notes/2377677.2377767_(1)_notes.md` | 3312 | 53 | `c774e03686f3` |
| `research_papers/notes/2377677.2377767_notes.md` | 3772 | 54 | `2e160f17174d` |
| `research_papers/notes/CLASS_ORIENTATION_GAP_CHECK.md` | 2490 | 75 | `a65d1046bcf9` |
| `research_papers/notes/NOTES_INDEX.md` | 1135 | 41 | `1bd479dbd1f8` |
| `research_papers/notes/PG_Orientation_Slides_AdigunMO.pptx` | 94919 | binary | `7c406106e420` |
| `research_papers/notes/SDN-based_Solutions_notes.md` | 3827 | 54 | `b2a67de2ea72` |
| `research_papers/notes/WhatsApp Imag.jpeg` | 65337 | binary | `c4ea7c0a56ad` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at .jpeg` | 67035 | binary | `510b0a40fb37` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.16.57.jpeg` | 23754 | binary | `77fc79ad0c81` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.16.58.jpeg` | 63099 | binary | `b16bc1dac575` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.16.59.jpeg` | 67319 | binary | `beac5ec4af6b` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.17.00.jpeg` | 64108 | binary | `6f5c941618ca` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.17.01.jpeg` | 53120 | binary | `e9477e07e668` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.17.02.jpeg` | 66888 | binary | `d0509c632a22` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.17.03.jpeg` | 64484 | binary | `ba4b7cbb4e29` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.17.04.jpeg` | 20083 | binary | `ab7f1e3ac00a` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.17.05.jpeg` | 16226 | binary | `62534f903a9a` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.17.06.jpeg` | 64217 | binary | `04d1db326c40` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.17.07.jpeg` | 67394 | binary | `e2587130caa0` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.17.08.jpeg` | 64951 | binary | `9aecabef21e2` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 02.jpeg` | 19769 | binary | `def39d33f57a` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 10.jpeg` | 60167 | binary | `d6a6fb7f7051` |
| `research_papers/notes/WhatsApp Image 2026-03-20 at 17.09.jpeg` | 66624 | binary | `746bc858fb82` |
| `research_papers/notes/computers-11-00111_notes.md` | 3585 | 54 | `61250e255494` |
| `research_papers/notes/peerj-cs-1698_notes.md` | 3635 | 54 | `100f6681f419` |
| `research_papers/notes/smartcities-08-00025_notes.md` | 4076 | 55 | `33c61b16c642` |
| `research_papers/notes/symmetry-15-01520-v2_notes.md` | 3905 | 54 | `7b6a2208afae` |
| `research_papers/notes/workshop notes/WhatsApp .jpeg` | 162986 | binary | `efe29704aad9` |
| `research_papers/notes/workshop notes/WhatsApp Image 2026-03-26 .jpeg` | 163038 | binary | `c7ffdacd15f7` |
| `research_papers/notes/workshop notes/WhatsApp Image 2026-03-26 at 00..jpeg` | 154781 | binary | `50d255d58b19` |
| `research_papers/notes/workshop notes/WhatsApp Image 2026-03-26 at 00.15.0.jpeg` | 167485 | binary | `9de8935403b3` |
| `research_papers/notes/workshop notes/WhatsApp Image 2026-03-26 at 00.15.08.jpeg` | 184947 | binary | `b41ab50d15c8` |
| `research_papers/notes/workshop notes/WhatsApp Image 2026-03-26 at 00.15.09.jpeg` | 151139 | binary | `249d3f36ce8d` |
| `research_papers/notes/workshop notes/WhatsApp Image 2026-03-26 at 00.15.10.jpeg` | 144856 | binary | `830efa40eaeb` |
| `research_papers/notes/workshop notes/WhatsApp Image 2026-03-26 at 00.15.jpeg` | 186480 | binary | `788f0f24561a` |
| `research_papers/notes/workshop notes/WhatsApp Image 2026-03-26 at 00.jpeg` | 145100 | binary | `147099571475` |
| `research_papers/peerj-cs-1698.pdf` | 14812064 | binary | `05685bde25ca` |
| `research_papers/sdn_textbooks/About-the-Authors_2017_Software-Defined-Networks.pdf` | 35046 | binary | `42b110d5234c` |
| `research_papers/sdn_textbooks/Acknowledgments_2017_Software-Defined-Networks.pdf` | 25158 | binary | `e6d671f5805a` |
| `research_papers/sdn_textbooks/Appendix-A---Acronyms-and-Abbreviations_2017_Software-Defined-Networks.pdf` | 38080 | binary | `b82c47835486` |
| `research_papers/sdn_textbooks/Appendix-B---Blacklist-Application_2017_Software-Defined-Networks.pdf` | 52831 | binary | `0189b9e9236d` |
| `research_papers/sdn_textbooks/Chapter-1---Introduction_2017_Software-Defined-Networks.pdf` | 1293183 | binary | `557361c3b293` |
| `research_papers/sdn_textbooks/Chapter-10---Network-Functions-Virtualization_2017_Software-Defined-Networks.pdf` | 864291 | binary | `612343e60559` |
| `research_papers/sdn_textbooks/Chapter-11---Players-in-the-SDN-Ecosystem_2017_Software-Defined-Networks.pdf` | 3048653 | binary | `f214b4a1b190` |
| `research_papers/sdn_textbooks/Chapter-12---SDN-Applications_2017_Software-Defined-Networks.pdf` | 490034 | binary | `5c8191212a9d` |
| `research_papers/sdn_textbooks/Chapter-13---SDN-Open-Source_2017_Software-Defined-Networks.pdf` | 1634121 | binary | `4abb9cd0419e` |
| `research_papers/sdn_textbooks/Chapter-14---Business-Ramifications_2017_Software-Defined-Networks.pdf` | 252245 | binary | `667b3d365860` |
| `research_papers/sdn_textbooks/Chapter-15---SDN-Futures_2017_Software-Defined-Networks.pdf` | 274162 | binary | `69e0168c6abd` |
| `research_papers/sdn_textbooks/Chapter-2---Why-SDN-_2017_Software-Defined-Networks.pdf` | 488423 | binary | `e1d781c3df69` |
| `research_papers/sdn_textbooks/Chapter-3---Genesis-of-SDN_2017_Software-Defined-Networks.pdf` | 824095 | binary | `b2385e0846ee` |
| `research_papers/sdn_textbooks/Chapter-4---How-SDN-Works_2017_Software-Defined-Networks.pdf` | 619830 | binary | `b4a2e540a2c1` |
| `research_papers/sdn_textbooks/Chapter-5---The-OpenFlow-Specification_2017_Software-Defined-Networks.pdf` | 1169384 | binary | `1ccf78ff6062` |
| `research_papers/sdn_textbooks/Chapter-6---Alternative-Definitions-of-SDN_2017_Software-Defined-Networks.pdf` | 724493 | binary | `b29c4827010c` |
| `research_papers/sdn_textbooks/Chapter-7---Emerging-Protocol--Controller--and-Appl_2017_Software-Defined-Ne.pdf` | 524930 | binary | `b0eacc75336f` |
| `research_papers/sdn_textbooks/Chapter-8---SDN-in-the-Data-Center_2017_Software-Defined-Networks.pdf` | 468506 | binary | `4d9273c6e13e` |
| `research_papers/sdn_textbooks/Chapter-9---SDN-in-Other-Environments_2017_Software-Defined-Networks.pdf` | 518719 | binary | `20c417501f78` |
| `research_papers/sdn_textbooks/Copyright_2017_Software-Defined-Networks.pdf` | 153298 | binary | `d668e0d32f36` |
| `research_papers/sdn_textbooks/Dedication_2017_Software-Defined-Networks.pdf` | 12749 | binary | `33191ba16255` |
| `research_papers/sdn_textbooks/Foreword_2017_Software-Defined-Networks.pdf` | 32352 | binary | `c996c9c41d50` |
| `research_papers/sdn_textbooks/Front-Matter_2017_Software-Defined-Networks.pdf` | 134119 | binary | `eb7f208ebb64` |
| `research_papers/sdn_textbooks/Index_2017_Software-Defined-Networks.pdf` | 69207 | binary | `e395e523f959` |
| `research_papers/sdn_textbooks/Preface_2017_Software-Defined-Networks.pdf` | 30336 | binary | `0acaac511279` |
| `research_papers/sdn_textbooks/README.md` | 544 | 16 | `40abab9911b7` |
| `research_papers/smartcities-08-00025.pdf` | 953313 | binary | `89db7f9933a8` |
| `research_papers/symmetry-15-01520-v2.pdf` | 3937939 | binary | `f5e2b846cac8` |
| `research_papers/templates/SATNAC_2025_Camera-Ready_0198.pdf` | 1142660 | binary | `40f48adfcfba` |
| `research_papers/templates/paper_extraction_template.md` | 983 | 52 | `97ff237ec504` |
| `results/dqn_1000_episodes_convergence.png` | 407269 | binary | `abdb5743b323` |
| `results/experiment_data/.gitkeep` | 42 | binary | `050ea8a84a07` |
| `results/experiment_data/baseline_internet2_summary.csv` | 458 | 3 | `334ac60262d0` |
| `results/experiment_data/baseline_telemetry_internet2.csv` | 15571 | 229 | `ab01a401aa1e` |
| `results/experiment_data/benchmark_20260309_041713.csv` | 517 | 7 | `13cf3b8eeb09` |
| `results/experiment_data/benchmark_20260309_042841.csv` | 569 | 7 | `32e39c0ade3d` |
| `results/experiment_data/benchmark_20260309_044211.csv` | 565 | 7 | `0ebec665eaff` |
| `results/experiment_data/benchmark_20260309_044937.csv` | 2814 | 27 | `610a6955e47f` |
| `results/experiment_data/benchmark_20260309_161635.csv` | 2814 | 27 | `610a6955e47f` |
| `results/experiment_data/benchmark_20260309_230955.csv` | 5446 | 52 | `a6a6f720fa2c` |
| `results/experiment_data/complete_proposal_aligned_benchmark.csv` | 5448 | 62 | `6fcde608ef95` |
| `results/experiment_data/factorial_latency_cost_best_20260314_050634.csv` | 558 | 4 | `620cbdf5b00c` |
| `results/experiment_data/factorial_latency_cost_best_20260314_050837.csv` | 558 | 4 | `086b0abf4da3` |
| `results/experiment_data/factorial_latency_cost_best_20260322_052249.csv` | 2317 | 14 | `cf3ca6553a70` |
| `results/experiment_data/factorial_latency_cost_best_20260326_021307.csv` | 2311 | 14 | `5eadd0bf084c` |
| `results/experiment_data/factorial_latency_cost_best_20260808_015946.csv` | 1627 | 10 | `a0624173fa94` |
| `results/experiment_data/factorial_latency_cost_best_20261017_052319.csv` | 2289 | 14 | `ff2ec2e40428` |
| `results/experiment_data/factorial_latency_cost_raw_20260314_050634.csv` | 1267 | 12 | `540ad077344c` |
| `results/experiment_data/factorial_latency_cost_raw_20260314_050837.csv` | 1266 | 12 | `0c0979e911c2` |
| `results/experiment_data/factorial_latency_cost_raw_20260322_052249.csv` | 34815 | 302 | `1741a5fedfea` |
| `results/experiment_data/factorial_latency_cost_raw_20260326_021307.csv` | 34809 | 302 | `ab4176b664a9` |
| `results/experiment_data/factorial_latency_cost_raw_20260808_015946.csv` | 13856 | 122 | `7c5984891c91` |
| `results/experiment_data/factorial_latency_cost_raw_20261017_052319.csv` | 33815 | 302 | `03b047d2b7f2` |
| `results/experiment_data/factorial_latency_cost_stats_20260322_052249.csv` | 8658 | 50 | `9915620c4fc5` |
| `results/experiment_data/factorial_latency_cost_stats_20260326_021307.csv` | 8646 | 50 | `7d6960daacac` |
| `results/experiment_data/factorial_latency_cost_stats_20260808_015946.csv` | 5979 | 34 | `019bac298d1e` |
| `results/experiment_data/factorial_latency_cost_stats_20261017_052319.csv` | 8610 | 50 | `92feaf9b9882` |
| `results/experiment_data/factorial_latency_cost_summary_20260314_050634.csv` | 1653 | 12 | `9e5e1aeaf3bb` |
| `results/experiment_data/factorial_latency_cost_summary_20260314_050837.csv` | 1666 | 12 | `b5952ce0e897` |
| `results/experiment_data/factorial_latency_cost_summary_20260322_052249.csv` | 10136 | 62 | `bc1a11605fe6` |
| `results/experiment_data/factorial_latency_cost_summary_20260326_021307.csv` | 10146 | 62 | `0c502150f306` |
| `results/experiment_data/factorial_latency_cost_summary_20260808_015946.csv` | 6956 | 42 | `84dc81295a34` |
| `results/experiment_data/factorial_latency_cost_summary_20261017_052319.csv` | 10045 | 62 | `e1c1a3e741b0` |
| `results/experiment_data/ga_challenger_internet2.csv` | 851 | 4 | `4de0084341e9` |
| `results/experiment_data/ga_seed_sweep_internet2.csv` | 388 | 5 | `e5e8490a0629` |
| `results/experiment_data/stress_test_best_compromise_20260309_050103.csv` | 399 | 4 | `e608a8927ec7` |
| `results/experiment_data/stress_test_best_compromise_20260326_021046.csv` | 1588 | 11 | `b8fb00baf668` |
| `results/experiment_data/stress_test_correlation_20260309_044057.csv` | 132 | 8 | `65a9aadd1074` |
| `results/experiment_data/stress_test_correlation_20260309_044132.csv` | 132 | 8 | `65a9aadd1074` |
| `results/experiment_data/stress_test_correlation_20260309_045102.csv` | 132 | 8 | `c235657e251c` |
| `results/experiment_data/stress_test_correlation_20260309_045617.csv` | 132 | 8 | `65a9aadd1074` |
| `results/experiment_data/stress_test_correlation_20260309_050103.csv` | 132 | 8 | `65a9aadd1074` |
| `results/experiment_data/stress_test_correlation_20260326_021046.csv` | 328 | 8 | `744b70979a35` |
| `results/experiment_data/stress_test_pareto_20260309_045617.csv` | 531 | 6 | `d4b2bdd66b7d` |
| `results/experiment_data/stress_test_pareto_20260309_050103.csv` | 437 | 5 | `596878a355af` |
| `results/experiment_data/stress_test_pareto_20260326_021046.csv` | 1479 | 11 | `fddf7db2a0da` |
| `results/experiment_data/stress_test_pareto_ranked_20260309_050103.csv` | 498 | 5 | `660126f99d5d` |
| `results/experiment_data/stress_test_pareto_ranked_20260326_021046.csv` | 1588 | 11 | `b8fb00baf668` |
| `results/experiment_data/stress_test_raw_20260309_044057.csv` | 1331 | 12 | `6e19f22d0384` |
| `results/experiment_data/stress_test_raw_20260309_044132.csv` | 1331 | 12 | `6e19f22d0384` |
| `results/experiment_data/stress_test_raw_20260309_045102.csv` | 17746 | 137 | `c859ca7724ac` |
| `results/experiment_data/stress_test_raw_20260309_045617.csv` | 1323 | 12 | `2fea49992256` |
| `results/experiment_data/stress_test_raw_20260309_050103.csv` | 1322 | 12 | `14932504a5b9` |
| `results/experiment_data/stress_test_raw_20260326_021046.csv` | 21025 | 137 | `f3745d35b9c8` |
| `results/experiment_data/stress_test_summary_20260309_044057.csv` | 1023 | 12 | `bcade6e0f5dc` |
| `results/experiment_data/stress_test_summary_20260309_044132.csv` | 1023 | 12 | `bcade6e0f5dc` |
| `results/experiment_data/stress_test_summary_20260309_045102.csv` | 4568 | 47 | `243eba306c27` |
| `results/experiment_data/stress_test_summary_20260309_045617.csv` | 1089 | 12 | `34232729f1fb` |
| `results/experiment_data/stress_test_summary_20260309_050103.csv` | 1089 | 12 | `4922fb05270f` |
| `results/experiment_data/stress_test_summary_20260326_021046.csv` | 6318 | 47 | `2a0340152416` |
| `results/graphs/.gitkeep` | 42 | binary | `050ea8a84a07` |
| `results/graphs/average_distance_20260309_041713.png` | 50478 | binary | `d2bc4baca0fe` |
| `results/graphs/average_distance_20260309_042841.png` | 46033 | binary | `012c203cd521` |
| `results/graphs/average_distance_20260309_044211.png` | 44323 | binary | `1b91d85c734b` |
| `results/graphs/average_distance_20260309_044937.png` | 46928 | binary | `8511784a8fb0` |
| `results/graphs/average_distance_20260309_161635.png` | 46928 | binary | `8511784a8fb0` |
| `results/graphs/average_distance_20260309_230955.png` | 45825 | binary | `328091c8fb1f` |
| `results/graphs/baseline_tau_internet2.png` | 108210 | binary | `9fd6e0da9724` |
| `results/graphs/control_plane_reliability_20260309_042841.png` | 45941 | binary | `bb3edeabd355` |
| `results/graphs/control_plane_reliability_20260309_044211.png` | 45941 | binary | `bb3edeabd355` |
| `results/graphs/control_plane_reliability_20260309_044937.png` | 45941 | binary | `bb3edeabd355` |
| `results/graphs/control_plane_reliability_20260309_161635.png` | 45941 | binary | `bb3edeabd355` |
| `results/graphs/control_plane_reliability_20260309_230955.png` | 45941 | binary | `bb3edeabd355` |
| `results/graphs/controller_load_std_20260309_041713.png` | 44205 | binary | `369fc7fc961e` |
| `results/graphs/controller_load_std_20260309_042841.png` | 44286 | binary | `72aa75fb0a63` |
| `results/graphs/controller_load_std_20260309_044211.png` | 40414 | binary | `158719db3a7b` |
| `results/graphs/controller_load_std_20260309_044937.png` | 41649 | binary | `83cb7550a669` |
| `results/graphs/controller_load_std_20260309_161635.png` | 41649 | binary | `83cb7550a669` |
| `results/graphs/controller_load_std_20260309_230955.png` | 40856 | binary | `07d4044f3c3e` |
| `results/graphs/latency_cost_pareto_20260314_050634/latency_cost_pareto_barabasi_albert_n20_k3_20260314_050634.png` | 77089 | binary | `b301dec3fa3d` |
| `results/graphs/latency_cost_pareto_20260314_050634/latency_cost_pareto_waxman_n20_k3_20260314_050634.png` | 73512 | binary | `9fe243ea8af4` |
| `results/graphs/latency_cost_pareto_20260314_050837/latency_cost_pareto_barabasi_albert_n20_k3_20260314_050837.png` | 76511 | binary | `70b8a8c8e25c` |
| `results/graphs/latency_cost_pareto_20260314_050837/latency_cost_pareto_waxman_n20_k3_20260314_050837.png` | 75348 | binary | `c3f8d79c442c` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_barabasi_albert_n100_k3_20260322_052249.png` | 74299 | binary | `12c881334e8f` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_barabasi_albert_n100_k5_20260322_052249.png` | 78642 | binary | `824ab3242faa` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_barabasi_albert_n20_k3_20260322_052249.png` | 78377 | binary | `e48dc4c00203` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_barabasi_albert_n20_k5_20260322_052249.png` | 83489 | binary | `30766ae95a72` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_barabasi_albert_n50_k3_20260322_052249.png` | 75591 | binary | `74785486ddeb` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_barabasi_albert_n50_k5_20260322_052249.png` | 77606 | binary | `0139b901e662` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_waxman_n100_k3_20260322_052249.png` | 76290 | binary | `8e57e5ec7913` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_waxman_n100_k5_20260322_052249.png` | 73350 | binary | `4c9f2b30bb34` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_waxman_n20_k3_20260322_052249.png` | 76689 | binary | `32849aa4543a` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_waxman_n20_k5_20260322_052249.png` | 77955 | binary | `4dc4d3d2a770` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_waxman_n50_k3_20260322_052249.png` | 75126 | binary | `ef045327b734` |
| `results/graphs/latency_cost_pareto_20260322_052249/latency_cost_pareto_waxman_n50_k5_20260322_052249.png` | 75709 | binary | `e3c6f96104a6` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_barabasi_albert_n100_k3_20260326_021307.png` | 74306 | binary | `bd2cda9fbdc6` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_barabasi_albert_n100_k5_20260326_021307.png` | 78745 | binary | `1737ff5deca7` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_barabasi_albert_n20_k3_20260326_021307.png` | 78107 | binary | `ca10725a260e` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_barabasi_albert_n20_k5_20260326_021307.png` | 83297 | binary | `d325662c3ab7` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_barabasi_albert_n50_k3_20260326_021307.png` | 75405 | binary | `58b4e3f52044` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_barabasi_albert_n50_k5_20260326_021307.png` | 77644 | binary | `f2c81a26134b` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_waxman_n100_k3_20260326_021307.png` | 76792 | binary | `3c6ace040b89` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_waxman_n100_k5_20260326_021307.png` | 73569 | binary | `8e346f33edbc` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_waxman_n20_k3_20260326_021307.png` | 76084 | binary | `f8758a478bb6` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_waxman_n20_k5_20260326_021307.png` | 77138 | binary | `82f134ee50be` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_waxman_n50_k3_20260326_021307.png` | 75038 | binary | `0329d74e3b5e` |
| `results/graphs/latency_cost_pareto_20260326_021307/latency_cost_pareto_waxman_n50_k5_20260326_021307.png` | 76116 | binary | `d12905b3aef7` |
| `results/graphs/latency_cost_pareto_20260808_015946/latency_cost_pareto_barabasi_albert_n20_k3_20260808_015946.png` | 87572 | binary | `a809783b62b0` |
| `results/graphs/latency_cost_pareto_20260808_015946/latency_cost_pareto_barabasi_albert_n20_k5_20260808_015946.png` | 94765 | binary | `08d0fcdf0046` |
| `results/graphs/latency_cost_pareto_20260808_015946/latency_cost_pareto_barabasi_albert_n50_k3_20260808_015946.png` | 90771 | binary | `c3ba100f03e1` |
| `results/graphs/latency_cost_pareto_20260808_015946/latency_cost_pareto_barabasi_albert_n50_k5_20260808_015946.png` | 86798 | binary | `5fe7c888bcea` |
| `results/graphs/latency_cost_pareto_20260808_015946/latency_cost_pareto_waxman_n20_k3_20260808_015946.png` | 91255 | binary | `02baa9fda0ab` |
| `results/graphs/latency_cost_pareto_20260808_015946/latency_cost_pareto_waxman_n20_k5_20260808_015946.png` | 87860 | binary | `ff701de6d934` |
| `results/graphs/latency_cost_pareto_20260808_015946/latency_cost_pareto_waxman_n50_k3_20260808_015946.png` | 86964 | binary | `179a18c1bbd2` |
| `results/graphs/latency_cost_pareto_20260808_015946/latency_cost_pareto_waxman_n50_k5_20260808_015946.png` | 84498 | binary | `ef1d68a71d29` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_barabasi_albert_n20_k2_20261017_052319.png` | 78101 | binary | `345a66073f65` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_barabasi_albert_n20_k3_20261017_052319.png` | 87476 | binary | `eb4fd9fac53a` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_barabasi_albert_n20_k5_20261017_052319.png` | 87715 | binary | `10adb2cfbc76` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_barabasi_albert_n50_k2_20261017_052319.png` | 84994 | binary | `f0c09f11f7ba` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_barabasi_albert_n50_k3_20261017_052319.png` | 93691 | binary | `ce4f833b81b2` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_barabasi_albert_n50_k5_20261017_052319.png` | 91568 | binary | `4a55aef49eda` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_waxman_n20_k2_20261017_052319.png` | 85125 | binary | `91a777bb7640` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_waxman_n20_k3_20261017_052319.png` | 86396 | binary | `c26c52f09bf5` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_waxman_n20_k5_20261017_052319.png` | 85325 | binary | `1b13e80de6c3` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_waxman_n50_k2_20261017_052319.png` | 84515 | binary | `3eeb972c7ff0` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_waxman_n50_k3_20261017_052319.png` | 84635 | binary | `5f6066c6fddf` |
| `results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_waxman_n50_k5_20261017_052319.png` | 82113 | binary | `7b8e7a1faa75` |
| `results/graphs/latency_vs_reliability_20260309_044057.png` | 75546 | binary | `9029d662a87c` |
| `results/graphs/latency_vs_reliability_20260309_044132.png` | 75546 | binary | `9029d662a87c` |
| `results/graphs/latency_vs_reliability_20260309_045102.png` | 86080 | binary | `cb3f3820c3ef` |
| `results/graphs/latency_vs_reliability_20260309_045617.png` | 77690 | binary | `0bf37e0198a2` |
| `results/graphs/latency_vs_reliability_20260309_050103.png` | 90007 | binary | `1a37f194b94e` |
| `results/graphs/latency_vs_reliability_20260326_021046.png` | 96623 | binary | `cdd435ba6ff3` |
| `results/graphs/pareto_presentation.html` | 4850956 | binary | `2c07ee1c425a` |
| `results/graphs/pareto_presentation.png` | 103260 | binary | `92d35f073228` |
| `results/graphs/resilience_ratio_20260309_041713.png` | 41378 | binary | `6d902bde23b7` |
| `results/graphs/resilience_ratio_20260309_042841.png` | 40196 | binary | `ad7a5e557918` |
| `results/graphs/resilience_ratio_20260309_044211.png` | 40388 | binary | `bad8c3aa6d74` |
| `results/graphs/resilience_ratio_20260309_044937.png` | 45377 | binary | `bc75b92b7da0` |
| `results/graphs/resilience_ratio_20260309_161635.png` | 45377 | binary | `bc75b92b7da0` |
| `results/graphs/resilience_ratio_20260309_230955.png` | 45557 | binary | `7bc6edf34b1a` |
| `results/graphs/rl_training_20260309T021717.882802Z-539427.csv` | 1524 | 15 | `abef3deadf86` |
| `results/graphs/rl_training_20260309T021717.882802Z-539427.png` | 105476 | binary | `8f5202aba950` |
| `results/graphs/rl_training_20260309T025000.995593Z-573275.csv` | 1667 | 15 | `6401fae20594` |
| `results/graphs/rl_training_20260309T025000.995593Z-573275.png` | 125931 | binary | `9e63ab2a1cc4` |
| `results/graphs/worst_case_distance_20260309_041713.png` | 49571 | binary | `6f14255a9878` |
| `results/graphs/worst_case_distance_20260309_042841.png` | 52392 | binary | `eff40a1ddaf3` |
| `results/graphs/worst_case_distance_20260309_044211.png` | 43377 | binary | `d24fe838e6da` |
| `results/graphs/worst_case_distance_20260309_044937.png` | 46077 | binary | `a90e756a0d60` |
| `results/graphs/worst_case_distance_20260309_161635.png` | 46077 | binary | `a90e756a0d60` |
| `results/graphs/worst_case_distance_20260309_230955.png` | 45398 | binary | `47b182b9670f` |
| `results/mininet_overhead_validation.json` | 2257 | 58 | `f940ae8bb46d` |
| `results/mininet_simulation_results.json` | 694 | 47 | `e0a130bc02a3` |
| `results/pilot_metrics.json` | 24429 | 1033 | `12adf6f99c7f` |
| `results/rl_analysis/ANALYSIS_REPORT.md` | 7263 | 193 | `eb401b9bc8de` |
| `results/rl_analysis/convergence_analysis.png` | 694138 | binary | `cdee0c90ac3b` |
| `results/rl_analysis/pareto/pareto_frontier_interactive.html` | 10788 | binary | `edff90ae57c4` |
| `results/rl_analysis/pareto/pareto_frontier_static.png` | 304961 | binary | `c0ac027c1b16` |
| `results/rl_analysis/pareto/pareto_marked.csv` | 6470 | 62 | `c3337af2d738` |
| `results/rl_analysis/pareto/pareto_mininet_validation.json` | 3949 | 134 | `50b0b7dc054f` |
| `results/rl_analysis/pareto/pareto_shortlist.json` | 180 | 12 | `845cf9adae5e` |
| `results/rl_analysis/pareto/pareto_shortlist_reliability_sweep.json` | 7103 | 359 | `9dafd09af63a` |
| `results/rl_analysis/pareto_multisite/pareto_frontier_interactive.html` | 10716 | binary | `41016c8d5dc8` |
| `results/rl_analysis/pareto_multisite/pareto_frontier_static.png` | 298132 | binary | `da201e4d55a6` |
| `results/rl_analysis/pareto_multisite/pareto_marked.csv` | 4027 | 27 | `9a05e9e0a53a` |
| `results/rl_analysis/pareto_multisite/pareto_shortlist.json` | 1402 | 52 | `b0ff7ad20816` |
| `results/rl_analysis/reward_distribution.png` | 117673 | binary | `55240268a4e3` |
| `results/rl_analysis/stability_audit/stability_grouped_by_topology.csv` | 370 | 4 | `19d7eaffa5bf` |
| `results/rl_analysis/stability_audit/stability_summary.csv` | 1949 | 12 | `e96278ae255b` |
| `results/rl_analysis/stability_audit/stability_summary.json` | 5664 | 182 | `e2aadfc2cc4f` |
| `results/rl_analysis/stability_audit/training_events.jsonl` | 119905 | binary | `2ec266b423bd` |
| `results/rl_training/training_log.jsonl` | 12596 | binary | `3313efc87b7d` |
| `run_baseline_internet2.py` | 11340 | 350 | `57639e7e9e7f` |
| `run_rl_training.py` | 2183 | 75 | `c7959ea9579b` |
| `scripts/align_presentation_to_proposal.py` | 8514 | 188 | `6c945b97b142` |
| `scripts/audit_baseline_factorial_cell.py` | 8834 | 235 | `379a7e271efc` |
| `scripts/batch_hyperlink_update.py` | 7969 | 245 | `dcc9a0d62196` |
| `scripts/compute_complete_benchmark_matrix.py` | 5903 | 120 | `ffd8247c8eb5` |
| `scripts/export_chat_history.py` | 4937 | 134 | `3f7cae1abf04` |
| `scripts/generate_decision_flowchart.py` | 4006 | 87 | `96c41ea11d1b` |
| `scripts/generate_one_pager_pitch.py` | 6174 | 113 | `de2f12140c25` |
| `scripts/generate_pareto_presentation_plot.py` | 3375 | 95 | `c955ddc6816d` |
| `scripts/generate_proposal_docs.py` | 48780 | 424 | `3a1d02e5f3f8` |
| `scripts/generate_satnac_word_doc.py` | 46507 | 753 | `f2be238e7da3` |
| `scripts/generate_sdn_pareto_3d.py` | 5040 | 178 | `9746c4d04e2d` |
| `scripts/generate_sdn_pareto_3d_print.py` | 4486 | 158 | `2f6ad2bf2400` |
| `scripts/generate_table1_image.py` | 3711 | 102 | `7f1a2e48f377` |
| `scripts/generate_table2_image.py` | 3121 | 98 | `4b4d3ca9f12c` |
| `scripts/harden_bibliography_links_pdf.py` | 7861 | 225 | `1e5ae048f775` |
| `scripts/harden_pdf_internal_links.py` | 6344 | 182 | `fc116770ad64` |
| `scripts/harden_section_113_timeline_pdf.py` | 5642 | 144 | `d53a8178bc28` |
| `scripts/inspect_pdf_structure.py` | 553 | 16 | `bb4b413a52c8` |
| `scripts/migrate_submission_into_hardened.py` | 3948 | 124 | `733bf0655a0d` |
| `scripts/pareto_synthesis.py` | 7506 | 217 | `309569f765cc` |
| `scripts/patch_methodology.py` | 9539 | 148 | `61d9abc9a77d` |
| `scripts/patch_research_proposal_pdf.py` | 13675 | 304 | `1670049ec501` |
| `scripts/patch_section_3_update.py` | 3550 | 71 | `75c536ce08b1` |
| `scripts/pilot_summary.py` | 2184 | 72 | `140fcb7bec7e` |
| `scripts/plot_baseline_tau.py` | 4353 | 138 | `93daedab0e5d` |
| `scripts/plot_pilot_metrics.py` | 1612 | 42 | `cb4779b54623` |
| `scripts/plot_rl_training_log.py` | 6137 | 180 | `b21d6af6495f` |
| `scripts/quick_verify.py` | 1647 | 49 | `a041077d65c0` |
| `scripts/regenerate_pdf_clean.py` | 10190 | 143 | `314b1297d7a1` |
| `scripts/reliability_sweep_and_internet2_check.py` | 3598 | 82 | `fbec4989f350` |
| `scripts/render_final_submission_pdf.py` | 6543 | 187 | `76a99988b517` |
| `scripts/run_factorial_latency_cost_matrix.py` | 22315 | 579 | `bcd3a4772d6d` |
| `scripts/run_full_workflow.py` | 3316 | 111 | `567c73c06f2b` |
| `scripts/run_ga_challenger_internet2.py` | 8364 | 211 | `c2e090c13573` |
| `scripts/run_linux_ready_benchmark.py` | 1516 | 54 | `32ab68cec9ce` |
| `scripts/run_mininet_demo.py` | 2793 | 66 | `2146fdc2a2cf` |
| `scripts/run_segmented_workload.py` | 5953 | 179 | `1851626d7878` |
| `scripts/run_stability_audit.py` | 14850 | 432 | `d8aad75b78c1` |
| `scripts/show_pilot_results.py` | 4756 | 110 | `fc2833f5de45` |
| `scripts/show_pilot_summary.py` | 4308 | 110 | `10f52bed3421` |
| `scripts/stress_test_latency_reliability.py` | 11145 | 309 | `7203f4609a52` |
| `scripts/test_mininet_overhead.py` | 25444 | 643 | `f9149ff5f647` |
| `scripts/train_dqn_pilot.py` | 16330 | 432 | `249db350a134` |
| `scripts/validate_shortlist_mininet.py` | 8551 | 231 | `9c0420db3b99` |
| `scripts/verify_proposal_compliance.py` | 7438 | 232 | `96d76d7248bc` |
| `simulation/__init__.py` | 233 | 12 | `b5651f014ae3` |
| `simulation/mininet_simulation.py` | 6782 | 203 | `1685b59888a6` |
| `slides/pareto_presentation.png` | 103260 | binary | `92d35f073228` |
| `slides/presentation.md` | 1521 | 36 | `b06b6c21508a` |
| `slides/presentation.pdf` | 168102 | binary | `789fb64a7878` |
| `test_torch.py` | 231 | 8 | `6214650d91d4` |
| `tests/test_experiment_config.py` | 3792 | 105 | `8f7cc6dac4b7` |
| `tests/test_manifest_schema.py` | 3266 | 88 | `d7a2ffa8bac5` |
| `tests/test_pareto_frontier.py` | 5174 | 150 | `a364d5262bba` |
| `tests/test_reliability_metric.py` | 1087 | 30 | `bf8164f54018` |
| `tests/test_rl_logging.py` | 4388 | 126 | `fed56d360357` |
| `tests/test_telemetry.py` | 1507 | 44 | `fba8fb01e53f` |
| `tests/test_topology_loader.py` | 2705 | 75 | `65f4dc4b1856` |
| `topology/__init__.py` | 574 | 24 | `6c89d6766a03` |
| `topology/canonical_topologies.py` | 9187 | 275 | `e747434afe22` |
| `topology/network_topology.py` | 3831 | 117 | `8127ea1bbf5c` |
| `topology/synthetic_topology_models.py` | 5229 | 170 | `2ee2f86888a6` |
| `venv310/bin/Activate.ps1` | 9033 | binary | `3795a060dea7` |
| `venv310/bin/activate` | 2028 | binary | `51bce42859ea` |
| `venv310/bin/activate.csh` | 954 | binary | `231d5154fcd8` |
| `venv310/bin/activate.fish` | 2230 | binary | `8c1dbcef9216` |
| `venv310/bin/f2py` | 212 | binary | `e27825e2b0c9` |
| `venv310/bin/fonttools` | 213 | binary | `3c6e5f5cdf0d` |
| `venv310/bin/inv` | 220 | binary | `87287240e4b3` |
| `venv310/bin/invoke` | 220 | binary | `87287240e4b3` |
| `venv310/bin/ipython` | 220 | binary | `93d7c2f602c5` |
| `venv310/bin/ipython3` | 220 | binary | `93d7c2f602c5` |
| `venv310/bin/isympy` | 201 | binary | `0fec69b92f9c` |
| `venv310/bin/netaddr` | 210 | binary | `f5a803d86596` |
| `venv310/bin/normalizer` | 233 | binary | `b2c65944ba5e` |
| `venv310/bin/numpy-config` | 212 | binary | `125767baa454` |
| `venv310/bin/oslo-config-generator` | 220 | binary | `bf306cb87e7c` |
| `venv310/bin/oslo-config-validator` | 220 | binary | `ab43e9b15834` |
| `venv310/bin/ovs-flowviz` | 734 | binary | `a9f65f095559` |
| `venv310/bin/pbr` | 211 | binary | `0ebc140b6739` |
| `venv310/bin/pip` | 217 | binary | `e4224b52c4ea` |
| `venv310/bin/pip3` | 217 | binary | `e4224b52c4ea` |
| `venv310/bin/pip3.10` | 217 | binary | `e4224b52c4ea` |
| `venv310/bin/plotly_get_chrome` | 239 | binary | `1a226b12d1b3` |
| `venv310/bin/proton` | 217 | binary | `04f5329c28f4` |
| `venv310/bin/proton-viewer` | 217 | binary | `d5e1df9e7754` |
| `venv310/bin/pyftmerge` | 210 | binary | `bfeb7cb071a9` |
| `venv310/bin/pyftsubset` | 211 | binary | `645c98d9ad64` |
| `venv310/bin/pygmentize` | 211 | binary | `d38fd103cca0` |
| `venv310/bin/python` | 5236248 | binary | `d317b3c9c1bf` |
| `venv310/bin/python3` | 5236248 | binary | `d317b3c9c1bf` |
| `venv310/bin/python3.10` | 5236248 | binary | `d317b3c9c1bf` |
| `venv310/bin/ryu` | 215 | binary | `ad7d6b3fd77c` |
| `venv310/bin/ryu-manager` | 214 | binary | `e051bf7bfaca` |
| `venv310/bin/torchfrtrace` | 237 | binary | `4e3165b58c01` |
| `venv310/bin/torchrun` | 216 | binary | `75f79b5e72b5` |
| `venv310/bin/tqdm` | 203 | binary | `406c2273796d` |
| `venv310/bin/ttx` | 208 | binary | `05198a5533a4` |
| `venv310/bin/wheel` | 208 | binary | `aa1cf20bd5c9` |
| `venv310/etc/ryu/ryu.conf` | 145 | binary | `3c07bdd1b1f2` |
| `venv310/include/site/python3.10/greenlet/greenlet.h` | 4755 | binary | `b33e69611490` |
| `venv310/pyvenv.cfg` | 71 | binary | `852addd6d76e` |
| `venv310/share/jupyter/labextensions/jupyterlab-plotly/install.json` | 63 | 4 | `31fa7d2306ba` |
| `venv310/share/jupyter/labextensions/jupyterlab-plotly/package.json` | 1411 | 41 | `b020e5283da5` |
| `venv310/share/jupyter/labextensions/jupyterlab-plotly/static/1.9daa5160b7fc741623bf.js` | 4829088 | binary | `f0fe886d2801` |
| `venv310/share/jupyter/labextensions/jupyterlab-plotly/static/1.9daa5160b7fc741623bf.js.LICENSE.txt` | 2087 | 80 | `1c9ebb787344` |
| `venv310/share/jupyter/labextensions/jupyterlab-plotly/static/remoteEntry.b2077f01f9b03ba2c63d.js` | 3789 | binary | `b2077f01f9b0` |
| `venv310/share/jupyter/labextensions/jupyterlab-plotly/static/style.js` | 118 | binary | `f8242dd194cf` |
| `venv310/share/jupyter/labextensions/jupyterlab-plotly/static/third-party-licenses.json` | 1264 | 10 | `e202018f172d` |
| `venv310/share/man/man1/ipython.1` | 2058 | binary | `3d57503f6847` |
| `venv310/share/man/man1/isympy.1` | 6659 | binary | `f4365d48e210` |
| `venv310/share/man/man1/ttx.1` | 5377 | binary | `70b6e6fe938e` |

## 2. Core Source & Benchmark Snapshots

### `configs/experiment_config.json`
```
{
  "topology": {
    "num_sites": 4,
    "nodes_per_site": 12,
    "intra_site_degree": 4,
    "rewiring_prob": 0.2,
    "inter_site_links": 2,
    "seed": 42
  },
  "experiment": {
    "num_controllers": 3,
    "trials": 5,
    "seed": 42,
    "metrics_to_plot": [
      "average_distance",
      "worst_case_distance",
      "controller_load_std",
      "resilience_ratio",
      "control_plane_reliability"
    ]
  },
  "outputs": {
    "data_dir": "results/experiment_data",
    "graph_dir": "results/graphs",
    "logs_dir": "logs"
  },
  "rl_logging": {
    "enabled": true,
    "file_name": "rl_training.jsonl",
    "log_every": 25
  },
  "rl_objective": {
    "latency_weight": 1.0,
    "reliability_weight": 0.25,
    "seconds_per_episode_weight": 0.25
  },
  "rl_hyperparameters": {
    "comment": "Reference band from Farahi et al. (2026) AP-DQN implementation",
    "learning_rate": 0.001,
    "batch_size": 32,
    "gamma": 0.99,
    "max_episodes": 1000,
    "replay_memory_size": 10000,
    "target_update_frequency": 100,
    "epsilon_start": 1.0,
    "epsilon_end": 0.05,
    "epsilon_decay": 0.995
  },
  "topology_config": {
    "comment": "Primary canonical topologies: Internet2 and ATT-MPLS for baseline parity (Heller et al. 2012)",
    "primary_topologies": ["Internet2", "ATT-MPLS"],
    "synthetic_fallback": ["barabasi_albert", "waxman"],
    "internet2_nodes": 11,
    "att_mpls_nodes": 21
  },
  "simulation": {
    "comment": "Mininet + Iperf3 operationalization for packet-level realism",
    "emulator": "mininet",
    "traffic_generator": "iperf3",
    "traffic_duration_seconds": 10,
    "traffic_bandwidth_mbps": 100
  }
}

```

### `algorithms/baseline/random_placement.py`
```
from __future__ import annotations

import random
from typing import List

import networkx as nx


def random_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    seed: int | None = None,
) -> List[str]:
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    nodes = list(graph.nodes)
    if num_controllers > len(nodes):
        raise ValueError("num_controllers cannot exceed number of nodes")

    rng = random.Random(seed)
    return rng.sample(nodes, num_controllers)

```

### `algorithms/baseline/greedy_placement.py`
```
from __future__ import annotations

from typing import List

import networkx as nx


def greedy_k_center_placement(graph: nx.Graph, num_controllers: int) -> List[str]:
    """Farthest-first greedy placement (k-center style)."""
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    nodes = list(graph.nodes)
    if num_controllers > len(nodes):
        raise ValueError("num_controllers cannot exceed number of nodes")

    first_controller = max(nodes, key=lambda n: graph.degree[n])
    controllers = [first_controller]

    while len(controllers) < num_controllers:
        distances = nx.multi_source_dijkstra_path_length(graph, controllers, weight="weight")

        candidate = None
        farthest_distance = -1.0
        for node in nodes:
            if node in controllers:
                continue
            node_distance = distances.get(node, float("inf"))
            if node_distance > farthest_distance:
                farthest_distance = node_distance
                candidate = node

        if candidate is None:
            break
        controllers.append(candidate)

    return controllers

```

### `algorithms/baseline/kmeans_placement.py`
```
from __future__ import annotations

from typing import List

import networkx as nx
import numpy as np
from sklearn.cluster import KMeans


def _node_coordinates(graph: nx.Graph) -> tuple[list[str], np.ndarray]:
    nodes = list(graph.nodes)
    if all("x" in graph.nodes[node] and "y" in graph.nodes[node] for node in nodes):
        coords = np.array([[graph.nodes[node]["x"], graph.nodes[node]["y"]] for node in nodes], dtype=float)
    else:
        layout = nx.spring_layout(graph, seed=42)
        coords = np.array([layout[node] for node in nodes], dtype=float)
    return nodes, coords


def kmeans_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    random_state: int | None = 42,
) -> List[str]:
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    if num_controllers > graph.number_of_nodes():
        raise ValueError("num_controllers cannot exceed number of nodes")

    nodes, coords = _node_coordinates(graph)

    model = KMeans(n_clusters=num_controllers, n_init=10, random_state=random_state)
    model.fit(coords)

    placements: list[str] = []
    for centroid in model.cluster_centers_:
        distances = np.linalg.norm(coords - centroid, axis=1)
        for idx in np.argsort(distances):
            candidate = nodes[int(idx)]
            if candidate not in placements:
                placements.append(candidate)
                break

    return placements

```

### `algorithms/ai/genetic_algorithm.py`
```
from __future__ import annotations

import random
from typing import List, Tuple

import networkx as nx


from evaluation.metrics import control_plane_reliability_single_link_failure_cached


def _placement_score(
    all_pairs: dict,
    nodes: list[str],
    placement: Tuple[str, ...],
    graph: nx.Graph | None = None,
    worst_case_weight: float = 0.0,
    reliability_weight: float = 0.0,
) -> float:
    total_distance = 0.0
    max_distance = 0.0
    for node in nodes:
        d = min(all_pairs[node].get(controller, float("inf")) for controller in placement)
        total_distance += d
        if d > max_distance:
            max_distance = d
    avg_distance = total_distance / len(nodes)
    score = -(avg_distance + worst_case_weight * max_distance)
    if reliability_weight > 0.0 and graph is not None:
        rel = control_plane_reliability_single_link_failure_cached(graph, list(placement))
        score += reliability_weight * rel
    return score


def _crossover(
    parent_a: Tuple[str, ...],
    parent_b: Tuple[str, ...],
    num_controllers: int,
    nodes: list[str],
    rng: random.Random,
) -> Tuple[str, ...]:
    if num_controllers == 1:
        return parent_a

    split = rng.randint(1, num_controllers - 1)
    child = list(parent_a[:split])
    for gene in parent_b:
        if gene not in child:
            child.append(gene)
        if len(child) == num_controllers:
            break

    if len(child) < num_controllers:
        remaining = [node for node in nodes if node not in child]
        rng.shuffle(remaining)
        child.extend(remaining[: num_controllers - len(child)])

    return tuple(sorted(child))


def _mutate(
    individual: Tuple[str, ...],
    mutation_rate: float,
    nodes: list[str],
    rng: random.Random,
) -> Tuple[str, ...]:
    if rng.random() >= mutation_rate:
        return individual

    genes = list(individual)
    replace_idx = rng.randrange(len(genes))
    options = [node for node in nodes if node not in genes]
    if options:
        genes[replace_idx] = rng.choice(options)
    return tuple(sorted(genes))


def genetic_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    population_size: int = 40,
    generations: int = 50,
    mutation_rate: float = 0.15,
    tournament_size: int = 3,
    seed: int | None = 42,
    worst_case_weight: float = 0.0,
    reliability_weight: float = 0.0,
    return_metadata: bool = False,
) -> List[str] | tuple[List[str], dict[str, int | float | None]]:
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    nodes = list(graph.nodes)
    if num_controllers > len(nodes):
        raise ValueError("num_controllers cannot exceed number of nodes")

    rng = random.Random(seed)
    all_pairs = dict(nx.all_pairs_dijkstra_path_length(graph, weight="weight"))

    population = [tuple(sorted(rng.sample(nodes, num_controllers))) for _ in range(population_size)]
    best_so_far = float("-inf")
    best_so_far_history: list[float] = []
    best_placement_history: list[Tuple[str, ...]] = []

    for _ in range(generations):
        scores = {
            individual: _placement_score(
                all_pairs, nodes, individual, graph=graph,
                worst_case_weight=worst_case_weight, reliability_weight=reliability_weight
            )
            for individual in population
        }
        generation_best = max(population, key=lambda individual: scores[individual])
        best_so_far = max(best_so_far, max(scores.values()))
        best_so_far_history.append(best_so_far)
        best_placement_history.append(generation_best)
        elite = generation_best

        new_population = [elite]
        while len(new_population) < population_size:
            contenders_a = rng.sample(population, min(tournament_size, len(population)))
            contenders_b = rng.sample(population, min(tournament_size, len(population)))
            parent_a = max(contenders_a, key=lambda individual: scores[individual])
            parent_b = max(contenders_b, key=lambda individual: scores[individual])

            child = _crossover(parent_a, parent_b, num_controllers, nodes, rng)
            child = _mutate(child, mutation_rate, nodes, rng)
            new_population.append(child)

        population = new_population

    final_scores = {
        individual: _placement_score(
            all_pairs, nodes, individual, graph=graph,
            worst_case_weight=worst_case_weight, reliability_weight=reliability_weight
        )
        for individual in population
    }
    best = max(population, key=lambda individual: final_scores[individual])
    final_best_score = float(final_scores[best])

    best_so_far = max(best_so_far, final_best_score)
    best_so_far_history.append(best_so_far)
    best_placement_history.append(best)
    convergence_generation = next(
        (
            index + 1
            for index, score in enumerate(best_so_far_history)
            if final_best_score - score <= 1e-12
        ),
        None,
    )

    if return_metadata:
        return list(best), {
            "iterations_budget": int(generations),
            "convergence_iteration": convergence_generation,
            "final_score": final_best_score,
            "best_placement_history": [list(placement) for placement in best_placement_history],
        }

    return list(best)

```

### `algorithms/ai/reinforcement_learning.py`
```
from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import itertools
import json
import math
from pathlib import Path
import random
import time
from typing import List, Tuple

import networkx as nx
import numpy as np

from evaluation.metrics import (
    average_controller_distance,
    control_plane_reliability_single_link_failure,
    control_plane_reliability_single_link_failure_cached,
)


def _average_distance_from_all_pairs(
    all_pairs: dict,
    nodes: list[str],
    placement: Tuple[str, ...],
) -> float:
    total = 0.0
    for node in nodes:
        total += min(all_pairs[node].get(controller, float("inf")) for controller in placement)
    return total / len(nodes)


def _composite_reward(
    average_distance: float,
    reliability: float,
    latency_weight: float,
    reliability_weight: float,
    seconds_per_episode: float = 0.0,
    seconds_per_episode_weight: float = 0.0,
) -> float:
    return (
        -(latency_weight * average_distance)
        + (reliability_weight * reliability)
        - (seconds_per_episode_weight * seconds_per_episode)
    )


def _append_jsonl(log_path: str, records: list[dict]) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def bandit_rl_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    episodes: int = 300,
    epsilon: float = 0.2,
    candidate_pool_size: int = 64,
    seed: int | None = 42,
    log_path: str | None = None,
    log_every: int = 25,
    run_label: str | None = None,
    latency_weight: float = 1.0,
    reliability_weight: float = 0.0,
    seconds_per_episode_weight: float = 0.0,
    return_metadata: bool = False,
) -> List[str] | tuple[List[str], dict[str, int | float | None]]:
    """Epsilon-greedy bandit baseline for adaptive controller placement."""
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    if log_every <= 0:
        raise ValueError("log_every must be greater than zero")

    if latency_weight < 0:
        raise ValueError("latency_weight must be non-negative")

    if reliability_weight < 0:
        raise ValueError("reliability_weight must be non-negative")

    if seconds_per_episode_weight < 0:
        raise ValueError("seconds_per_episode_weight must be non-negative")

    nodes = list(graph.nodes)
    if num_controllers > len(nodes):
        raise ValueError("num_controllers cannot exceed number of nodes")

    rng = random.Random(seed)
    all_pairs = dict(nx.all_pairs_dijkstra_path_length(graph, weight="weight"))

    sorted_by_degree = sorted(nodes, key=lambda node: graph.degree[node], reverse=True)
    actions: set[Tuple[str, ...]] = {tuple(sorted(sorted_by_degree[:num_controllers]))}

    max_unique_actions = math.comb(len(nodes), num_controllers)
    target_size = min(max_unique_actions, max(8, min(candidate_pool_size, len(nodes) * 4)))

    attempts = 0
    max_attempts = max(64, target_size * 20)
    while len(actions) < target_size:
        actions.add(tuple(sorted(rng.sample(nodes, num_controllers))))
        attempts += 1
        if attempts >= max_attempts:
            # Deterministic fallback avoids long collision tails near saturation.
            for combo in itertools.combinations(nodes, num_controllers):
                actions.add(tuple(sorted(combo)))
                if len(actions) >= target_size:
                    break
            break

    action_list = list(actions)

    action_avg_distances = {
        action: _average_distance_from_all_pairs(all_pairs, nodes, action)
        for action in action_list
    }
    action_reliabilities = {
        action: control_plane_reliability_single_link_failure(graph, action)
        for action in action_list
    }
    action_rewards = {
        action: _composite_reward(
            average_distance=action_avg_distances[action],
            reliability=action_reliabilities[action],
            latency_weight=latency_weight,
            reliability_weight=reliability_weight,
            seconds_per_episode_weight=seconds_per_episode_weight,
        )
        for action in action_list
    }

    q_values = {action: 0.0 for action in action_list}
    visits = {action: 0 for action in action_list}

    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')}-{rng.randint(0, 999999):06d}"
    effective_label = run_label or "bandit_rl"
    epsilon_value = epsilon
    best_reward = float("-inf")
    best_reward_history: list[float] = []
    event_records: list[dict] = []

    if log_path:
        event_records.append(
            {
                "event": "run_start",
                "run_id": run_id,
                "label": effective_label,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "num_nodes": len(nodes),
                "num_actions": len(action_list),
                "num_controllers": num_controllers,
                "episodes": episodes,
                "epsilon_start": epsilon,
                "seed": seed,
                "latency_weight": latency_weight,
                "reliability_weight": reliability_weight,
            }
        )

    for episode in range(1, episodes + 1):
        if rng.random() < epsilon_value:
            action = rng.choice(action_list)
        else:
            action = max(action_list, key=lambda a: q_values[a])

        reward = action_rewards[action]
        best_reward = max(best_reward, reward)
        best_reward_history.append(best_reward)
        visits[action] += 1
        q_values[action] += (reward - q_values[action]) / visits[action]
        epsilon_value = max(0.01, epsilon_value * 0.995)

        if log_path and (episode == 1 or episode == episodes or episode % log_every == 0):
            event_records.append(
                {
                    "event": "episode",
                    "run_id": run_id,
                    "label": effective_label,
                    "episode": episode,
                    "reward": reward,
                    "best_reward": best_reward,
                    "epsilon": epsilon_value,
                    "selected_action": list(action),
                    "selected_action_avg_distance": action_avg_distances[action],
                    "selected_action_reliability": action_reliabilities[action],
                    "selected_action_q": q_values[action],
                    "selected_action_visits": visits[action],
                }
            )

    best_action = max(action_list, key=lambda action: q_values[action])
    convergence_episode = next(
        (
            index + 1
            for index, reward in enumerate(best_reward_history)
            if best_reward - reward <= 1e-12
        ),
        None,
    )

    if log_path:
        top_actions = sorted(action_list, key=lambda action: q_values[action], reverse=True)[:5]
        event_records.append(
            {
                "event": "run_end",
                "run_id": run_id,
                "label": effective_label,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "final_epsilon": epsilon_value,
                "best_action": list(best_action),
                "best_action_q": q_values[best_action],
                "best_action_avg_distance": action_avg_distances[best_action],
                "best_action_reliability": action_reliabilities[best_action],
                "top_actions": [
                    {
                        "controllers": list(action),
                        "q_value": q_values[action],
                        "average_distance": action_avg_distances[action],
                        "reliability": action_reliabilities[action],
                        "reward": action_rewards[action],
                        "visits": visits[action],
                    }
                    for action in top_actions
                ],
            }
        )
        _append_jsonl(log_path, event_records)

    if return_metadata:
        return list(best_action), {
            "iterations_budget": int(episodes),
            "convergence_iteration": convergence_episode,
            "final_best_reward": float(best_reward),
            "num_actions": int(len(action_list)),
        }

    return list(best_action)


import torch
import torch.nn as nn
import torch.optim as optim


class _DQN(nn.Module):
    def __init__(self, n_in: int, n_out: int):
        super().__init__()
        self.fc1 = nn.Linear(n_in, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, n_out)
        self.relu = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc3(self.relu(self.fc2(self.relu(self.fc1(x)))))


def dqn_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    episodes: int = 200,
    learning_rate: float = 0.001,
    gamma: float = 0.99,
    batch_size: int = 32,
    replay_capacity: int = 10000,
    epsilon_start: float = 1.0,
    epsilon_end: float = 0.05,
    epsilon_decay: float = 0.995,
    seed: int = 42,
    load_model_path: str | None = None,
    save_model_path: str | None = None,
    return_metadata: bool = False,
) -> List[str] | Tuple[List[str], dict]:
    """
    Multi-controller PyTorch Deep Q-Network (DQN) placement algorithm.
    Architecture: MLP Input(N) -> Linear(64, ReLU) -> Linear(64, ReLU) -> Output(N).
    Selects k distinct controller nodes sequentially per episode and evaluates both
    offline training time (s) and online single forward-pass inference latency (ms).
    Supports saving trained weights (`save_model_path`) and zero-retraining online
    inference on dynamic topology churn states (`load_model_path`).
    """
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")
    nodes = list(graph.nodes)
    num_nodes = len(nodes)
    if num_controllers > num_nodes:
        raise ValueError("num_controllers cannot exceed number of nodes")

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = torch.device("cpu")

    q_net = _DQN(num_nodes, num_nodes).to(device)
    target_net = _DQN(num_nodes, num_nodes).to(device)
    target_net.load_state_dict(q_net.state_dict())
    optimizer = optim.Adam(q_net.parameters(), lr=learning_rate)
    loss_fn = nn.MSELoss()
    replay_buffer: deque = deque(maxlen=replay_capacity)

    # Precompute worst-case single-node distance for normalized reward scaling
    all_pairs = dict(nx.all_pairs_dijkstra_path_length(graph, weight="weight"))
    max_avg_dist = max(
        float(np.mean(list(dist_map.values()))) for dist_map in all_pairs.values()
    )
    max_avg_dist = max(max_avg_dist, 1e-6)

    # Structural feature vector (normalized degree centrality) blended with placement mask
    degrees = np.array([graph.degree[n] for n in nodes], dtype=np.float32)
    norm_degrees = degrees / max(float(np.max(degrees)), 1.0)

    epsilon = epsilon_start
    best_controllers: List[str] = nodes[:num_controllers]
    best_reward = float("-inf")
    update_steps = 0

    if load_model_path is not None:
        q_net.load_state_dict(
            torch.load(load_model_path, map_location=device, weights_only=True)
        )
        q_net.eval()
        training_time_sec = 0.0
        episodes = 0
    else:
        t_train_start = time.perf_counter()
        for _ in range(episodes):
            selected_indices: List[int] = []
            mask = np.zeros(num_nodes, dtype=np.float32)
            state = norm_degrees.copy()

            for step_idx in range(num_controllers):
                available = [i for i in range(num_nodes) if i not in selected_indices]
                if random.random() < epsilon:
                    action = random.choice(available)
                else:
                    with torch.no_grad():
                        s_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
                        q_vals = q_net(s_tensor).squeeze(0).cpu().numpy()
                        q_vals[selected_indices] = -1e9
                        action = int(np.argmax(q_vals))

                selected_indices.append(action)
                mask[action] = 1.0
                next_state = 0.5 * norm_degrees + 0.5 * mask
                done = step_idx == (num_controllers - 1)

                current_nodes = [nodes[i] for i in selected_indices]
                avg_lat = _average_distance_from_all_pairs(all_pairs, nodes, tuple(current_nodes))
                rel = control_plane_reliability_single_link_failure_cached(graph, current_nodes)
                reward = float(10.0 * ((max_avg_dist - avg_lat) / max_avg_dist) + 5.0 * rel)

                if done and reward > best_reward:
                    best_reward = reward
                    best_controllers = list(current_nodes)

                replay_buffer.append((state, action, reward, next_state, float(done)))
                state = next_state

                if len(replay_buffer) >= batch_size:
                    batch = random.sample(replay_buffer, batch_size)
                    b_s, b_a, b_r, b_ns, b_d = zip(*batch)
                    s_t = torch.tensor(np.array(b_s), dtype=torch.float32, device=device)
                    a_t = torch.tensor(b_a, dtype=torch.int64, device=device)
                    r_t = torch.tensor(b_r, dtype=torch.float32, device=device)
                    ns_t = torch.tensor(np.array(b_ns), dtype=torch.float32, device=device)
                    d_t = torch.tensor(b_d, dtype=torch.float32, device=device)

                    q_pred = q_net(s_t).gather(1, a_t.unsqueeze(1)).squeeze(1)
                    with torch.no_grad():
                        q_next = target_net(ns_t).max(dim=1)[0]
                        q_target = r_t + (1.0 - d_t) * gamma * q_next

                    loss = loss_fn(q_pred, q_target)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                    update_steps += 1
                    if update_steps % 100 == 0:
                        target_net.load_state_dict(q_net.state_dict())

            epsilon = max(epsilon_end, epsilon * epsilon_decay)

        training_time_sec = time.perf_counter() - t_train_start
        if save_model_path is not None:
            out_file = Path(save_model_path)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            torch.save(q_net.state_dict(), out_file)

    # Measure online single forward-pass inference latency (top-k Q-value selection)
    q_net.eval()
    eval_state = torch.tensor(norm_degrees, dtype=torch.float32, device=device).unsqueeze(0)
    with torch.no_grad():
        for _ in range(10):
            _ = torch.topk(q_net(eval_state), k=num_controllers, dim=1)
        t_inf_start = time.perf_counter()
        for _ in range(100):
            topk_indices = torch.topk(q_net(eval_state), k=num_controllers, dim=1).indices.squeeze(0)
        inference_time_ms = ((time.perf_counter() - t_inf_start) / 100.0) * 1000.0

    inferred_controllers = [nodes[int(i)] for i in topk_indices.tolist()]
    inferred_lat = _average_distance_from_all_pairs(all_pairs, nodes, tuple(inferred_controllers))
    inferred_rel = control_plane_reliability_single_link_failure_cached(graph, inferred_controllers)
    inferred_reward = float(10.0 * ((max_avg_dist - inferred_lat) / max_avg_dist) + 5.0 * inferred_rel)
    if inferred_reward >= best_reward:
        best_controllers = inferred_controllers

    if return_metadata:
        return best_controllers, {
            "episodes": episodes,
            "training_time_sec": float(training_time_sec),
            "omega_sec_per_episode": float(training_time_sec / max(episodes, 1)),
            "inference_time_ms": float(inference_time_ms),
            "final_best_reward": float(max(best_reward, inferred_reward)),
        }
    return best_controllers


```

### `evaluation/metrics.py`
```
from __future__ import annotations

from hashlib import sha256
from typing import Any, Dict, Iterable

import networkx as nx
import numpy as np


def _match_controllers(graph: nx.Graph, controllers: Iterable[Any]) -> list:
    """Return a list of controller node objects that exist in `graph`.

    Tries to match controllers to the graph's node objects using several
    strategies so callers may pass ints or strings interchangeably.
    """
    nodes_set = set(graph.nodes())

    # 1) Direct match
    matched = [c for c in controllers if c in nodes_set]
    if matched:
        return matched

    # 2) Match by stringified node labels -> return original node objects
    str_to_node = {str(n): n for n in graph.nodes()}
    matched = [str_to_node[s] for s in map(str, controllers) if s in str_to_node]
    if matched:
        return matched

    # 3) Try int conversion for string-like controllers
    matched = []
    for c in controllers:
        try:
            num = int(c)
        except Exception:
            continue
        if num in nodes_set:
            matched.append(num)
    return matched


# Global reliability cache keyed by topology fingerprint.
# Each entry stores component-label matrices for all single-link failure states.
RELIABILITY_CACHE: dict[str, dict[str, Any]] = {}


def _topology_key(graph: nx.Graph) -> str:
    """Build a stable cache key from sorted nodes and edges."""
    nodes = tuple(sorted(str(node) for node in graph.nodes()))
    edges = tuple(
        sorted(
            (min(str(u), str(v)), max(str(u), str(v)))
            for u, v in graph.edges()
        )
    )
    payload = repr((nodes, edges)).encode("utf-8")
    return sha256(payload).hexdigest()


def precompute_reliability_cache(graph: nx.Graph) -> str:
    """
    Precompute N-1 failure connectivity labels for a topology exactly once.

    Cached structure:
      - node_order: list[str]
      - node_index: dict[str, int]
      - edge_order: list[tuple[node, node]]
      - component_labels: np.ndarray[int32] shape (num_edges, num_nodes)
    """
    cache_key = _topology_key(graph)
    if cache_key in RELIABILITY_CACHE:
        return cache_key

    node_order = [str(node) for node in graph.nodes()]
    node_index = {node: idx for idx, node in enumerate(node_order)}
    edge_order = list(graph.edges())

    num_edges = len(edge_order)
    num_nodes = len(node_order)
    component_labels = np.full((num_edges, num_nodes), -1, dtype=np.int32)

    for edge_idx, (edge_u, edge_v) in enumerate(edge_order):
        failed_graph = graph.copy()
        failed_graph.remove_edge(edge_u, edge_v)

        for comp_id, component in enumerate(nx.connected_components(failed_graph)):
            for node in component:
                component_labels[edge_idx, node_index[str(node)]] = comp_id

    RELIABILITY_CACHE[cache_key] = {
        "node_order": node_order,
        "node_index": node_index,
        "edge_order": edge_order,
        "component_labels": component_labels,
    }
    return cache_key


def _distance_map(graph: nx.Graph, controllers: Iterable[Any]) -> Dict[str, float]:
    sources = _match_controllers(graph, controllers)
    if not sources:
        return {}
    return {str(node): distance for node, distance in nx.multi_source_dijkstra_path_length(graph, sources, weight="weight").items()}


def average_controller_distance(graph: nx.Graph, controllers: Iterable[str]) -> float:
    controller_list = _match_controllers(graph, controllers)
    if not controller_list:
        return float("inf")

    distances = _distance_map(graph, controller_list)
    values = [distances.get(str(node), float("inf")) for node in graph.nodes]
    finite_values = [value for value in values if np.isfinite(value)]
    return float(np.mean(finite_values)) if finite_values else float("inf")


def worst_case_controller_distance(graph: nx.Graph, controllers: Iterable[str]) -> float:
    controller_list = _match_controllers(graph, controllers)
    if not controller_list:
        return float("inf")

    distances = _distance_map(graph, controller_list)
    values = [distances.get(str(node), float("inf")) for node in graph.nodes]
    finite_values = [value for value in values if np.isfinite(value)]
    return float(np.max(finite_values)) if finite_values else float("inf")


def controller_load_std(graph: nx.Graph, controllers: Iterable[str]) -> float:
    controller_list = _match_controllers(graph, controllers)
    if not controller_list:
        return float("inf")

    controller_distances = {
        controller: nx.single_source_dijkstra_path_length(graph, controller, weight="weight")
        for controller in controller_list
    }

    loads = {controller: 0 for controller in controller_list}
    for node in graph.nodes:
        best_controller = min(
            controller_list,
            key=lambda controller: controller_distances[controller].get(node, float("inf")),
        )
        loads[best_controller] += 1

    return float(np.std(list(loads.values())))


def resilience_ratio_single_failure(graph: nx.Graph, controllers: Iterable[str]) -> float:
    """Average degradation ratio after one controller failure at a time."""
    controller_list = _match_controllers(graph, controllers)
    if len(controller_list) <= 1:
        return 1.0

    baseline = average_controller_distance(graph, controller_list)
    if not np.isfinite(baseline) or baseline == 0:
        return float("inf")

    degradations = []
    for failed in controller_list:
        remaining = [controller for controller in controller_list if controller != failed]
        degraded = average_controller_distance(graph, remaining)
        degradations.append(degraded / baseline)

    return float(np.mean(degradations))


def control_plane_reliability_single_link_failure(
    graph: nx.Graph,
    controllers: Iterable[str],
) -> float:
    """
    Estimate control-plane reliability under single-link failures.

    For each edge failure, compute the fraction of nodes that can still reach at
    least one controller. Return the mean fraction across all single-link failures.
    A value of 1.0 means all nodes remain controller-reachable for every edge loss.
    """
    controller_list = _match_controllers(graph, controllers)
    if not controller_list:
        return 0.0

    if graph.number_of_nodes() == 0:
        return 1.0

    if graph.number_of_edges() == 0:
        reachable_without_failures = nx.multi_source_dijkstra_path_length(
            graph,
            controller_list,
            weight="weight",
        )
        return float(len(reachable_without_failures) / graph.number_of_nodes())

    reachability_ratios: list[float] = []
    for edge_u, edge_v in graph.edges:
        failed_graph = graph.copy()
        failed_graph.remove_edge(edge_u, edge_v)

        reachable = nx.multi_source_dijkstra_path_length(
            failed_graph,
            controller_list,
            weight="weight",
        )
        reachability_ratios.append(len(reachable) / graph.number_of_nodes())

    return float(np.mean(reachability_ratios))


def control_plane_reliability_single_link_failure_cached(
    graph: nx.Graph,
    controllers: Iterable[str],
) -> float:
    """
    Cached N-1 reliability query using precomputed component labels.

    This avoids per-call graph copying and shortest-path recomputation by turning
    reliability evaluation into vectorized NumPy operations.
    """
    controller_list = [str(controller) for controller in controllers]
    if not controller_list:
        return 0.0

    if graph.number_of_nodes() == 0:
        return 1.0

    # Preserve original edge-case behavior for edgeless graphs.
    if graph.number_of_edges() == 0:
        unique_controllers = {str(controller) for controller in controller_list}
        return float(len(unique_controllers & {str(node) for node in graph.nodes()}) / graph.number_of_nodes())

    cache_key = precompute_reliability_cache(graph)
    cache_entry = RELIABILITY_CACHE[cache_key]
    node_index = cache_entry["node_index"]
    component_labels: np.ndarray = cache_entry["component_labels"]

    controller_idx = [node_index[node] for node in controller_list if node in node_index]
    if not controller_idx:
        return 0.0

    # labels shape: (E, N), controller labels shape: (E, K)
    controller_labels = component_labels[:, controller_idx]
    reachable_mask = (component_labels[:, :, None] == controller_labels[:, None, :]).any(axis=2)

    # For each edge-failure row, reachable ratio is fraction of reachable nodes.
    per_failure_ratio = reachable_mask.mean(axis=1)
    return float(np.mean(per_failure_ratio))


def assert_cache_parity(
    graph: nx.Graph,
    controllers: Iterable[str],
    tolerance: float = 1e-9,
) -> float:
    """Assert cached and non-cached reliability computations match within tolerance."""
    baseline = control_plane_reliability_single_link_failure(graph, controllers)
    cached = control_plane_reliability_single_link_failure_cached(graph, controllers)
    delta = abs(baseline - cached)
    if delta > tolerance:
        raise AssertionError(
            f"Reliability cache parity check failed: baseline={baseline:.12f}, "
            f"cached={cached:.12f}, delta={delta:.12f}, tolerance={tolerance}"
        )
    return delta


def summarize_metrics(
    graph: nx.Graph,
    controllers: Iterable[str],
    use_cached_reliability: bool = True,
) -> Dict[str, float]:
    controller_list = list(controllers)
    reliability_fn = (
        control_plane_reliability_single_link_failure_cached
        if use_cached_reliability
        else control_plane_reliability_single_link_failure
    )
    return {
        "average_distance": average_controller_distance(graph, controller_list),
        "worst_case_distance": worst_case_controller_distance(graph, controller_list),
        "controller_load_std": controller_load_std(graph, controller_list),
        "resilience_ratio": resilience_ratio_single_failure(graph, controller_list),
        "control_plane_reliability": reliability_fn(graph, controller_list),
    }

```

### `evaluation/pareto.py`
```
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def _pareto_mask_latency_reliability(latency: np.ndarray, reliability: np.ndarray) -> np.ndarray:
    """Return mask for non-dominated points (min latency, max reliability)."""
    keep = np.ones(len(latency), dtype=bool)

    for i in range(len(latency)):
        if not keep[i]:
            continue

        dominated_by_other = (
            (latency <= latency[i])
            & (reliability >= reliability[i])
            & ((latency < latency[i]) | (reliability > reliability[i]))
        )
        dominated_by_other[i] = False

        if dominated_by_other.any():
            keep[i] = False

    return keep


def mark_latency_reliability_pareto(
    df: pd.DataFrame,
    group_cols: Iterable[str] | None = None,
    latency_col: str = "average_distance",
    reliability_col: str = "control_plane_reliability",
    output_col: str = "is_pareto_optimal",
) -> pd.DataFrame:
    """
    Mark Pareto-optimal rows for latency/reliability trade-off.

    Optimization objective:
    - minimize latency_col
    - maximize reliability_col

    If group_cols is provided, Pareto front is computed independently per group.
    """
    if latency_col not in df.columns:
        raise ValueError(f"Missing latency column: {latency_col}")
    if reliability_col not in df.columns:
        raise ValueError(f"Missing reliability column: {reliability_col}")

    groups = list(group_cols or [])
    for col in groups:
        if col not in df.columns:
            raise ValueError(f"Missing group column: {col}")

    result = df.copy()
    result[output_col] = False

    if groups:
        grouped_iter = result.groupby(groups, sort=False, dropna=False)
    else:
        grouped_iter = [(None, result)]

    for _, group in grouped_iter:
        valid = group[[latency_col, reliability_col]].notna().all(axis=1)
        valid_group = group.loc[valid]
        if valid_group.empty:
            continue

        latency = valid_group[latency_col].to_numpy(dtype=float)
        reliability = valid_group[reliability_col].to_numpy(dtype=float)
        mask = _pareto_mask_latency_reliability(latency, reliability)

        result.loc[valid_group.index[mask], output_col] = True

    return result


def rank_latency_reliability_compromise(
    df: pd.DataFrame,
    group_cols: Iterable[str] | None = None,
    latency_col: str = "average_distance",
    reliability_col: str = "control_plane_reliability",
    distance_col: str = "ideal_point_distance",
    rank_col: str = "compromise_rank",
) -> pd.DataFrame:
    """
    Rank rows by normalized distance to the group ideal point.

    Ideal point per group:
    - latency at its minimum
    - reliability at its maximum

    Lower distance means a better compromise across both objectives.
    """
    if latency_col not in df.columns:
        raise ValueError(f"Missing latency column: {latency_col}")
    if reliability_col not in df.columns:
        raise ValueError(f"Missing reliability column: {reliability_col}")

    groups = list(group_cols or [])
    for col in groups:
        if col not in df.columns:
            raise ValueError(f"Missing group column: {col}")

    result = df.copy()
    result[distance_col] = np.nan
    result[rank_col] = np.nan

    if groups:
        grouped_iter = result.groupby(groups, sort=False, dropna=False)
    else:
        grouped_iter = [(None, result)]

    for _, group in grouped_iter:
        valid = group[[latency_col, reliability_col]].notna().all(axis=1)
        valid_group = group.loc[valid]
        if valid_group.empty:
            continue

        latency = valid_group[latency_col].to_numpy(dtype=float)
        reliability = valid_group[reliability_col].to_numpy(dtype=float)

        latency_min = float(latency.min())
        latency_max = float(latency.max())
        rel_min = float(reliability.min())
        rel_max = float(reliability.max())

        if latency_max > latency_min:
            latency_norm = (latency - latency_min) / (latency_max - latency_min)
        else:
            latency_norm = np.zeros_like(latency)

        if rel_max > rel_min:
            # Reliability is maximized, so distance is measured from group max.
            reliability_norm = (rel_max - reliability) / (rel_max - rel_min)
        else:
            reliability_norm = np.zeros_like(reliability)

        distances = np.sqrt(np.square(latency_norm) + np.square(reliability_norm))
        result.loc[valid_group.index, distance_col] = distances

        # Tie-break with latency (lower) then reliability (higher).
        sortable = valid_group.copy()
        sortable[distance_col] = distances
        sortable = sortable.sort_values(
            [distance_col, latency_col, reliability_col],
            ascending=[True, True, False],
        )
        ranks = pd.Series(np.arange(1, len(sortable) + 1), index=sortable.index)
        result.loc[sortable.index, rank_col] = ranks.astype(float)

    return result


def select_best_latency_reliability_compromise(
    df: pd.DataFrame,
    group_cols: Iterable[str] | None = None,
    latency_col: str = "average_distance",
    reliability_col: str = "control_plane_reliability",
    distance_col: str = "ideal_point_distance",
    rank_col: str = "compromise_rank",
) -> pd.DataFrame:
    """Return rank-1 compromise rows per group using ideal-point distance."""
    ranked = rank_latency_reliability_compromise(
        df,
        group_cols=group_cols,
        latency_col=latency_col,
        reliability_col=reliability_col,
        distance_col=distance_col,
        rank_col=rank_col,
    )

    best = ranked[ranked[rank_col] == 1].copy()
    groups = list(group_cols or [])
    sort_cols = groups + [latency_col, reliability_col]
    ascending = [True] * len(groups) + [True, False]
    if sort_cols:
        best = best.sort_values(sort_cols, ascending=ascending)
    return best

```

### `simulation/mininet_simulation.py`
```
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
import random
import re
from typing import Dict, Iterable
import warnings

import networkx as nx
import numpy as np


@dataclass
class SimulationResult:
    average_rtt_ms: float
    worst_rtt_ms: float
    per_node_latency_ms: Dict[str, float]


def _parse_ping_avg_ms(output: str) -> float | None:
    """Extract average RTT from Linux ping output."""
    patterns = [
        r"=\s*[\d\.]+/([\d\.]+)/[\d\.]+/[\d\.]+\s*ms",
        r"min/avg/max(?:/mdev|/stddev)?\s*=\s*[\d\.]+/([\d\.]+)/",
    ]
    for pattern in patterns:
        match = re.search(pattern, output)
        if match:
            return float(match.group(1))
    return None


def run_synthetic_latency_simulation(
    graph: nx.Graph,
    controllers: Iterable[str],
    base_link_delay_ms: float = 2.0,
    jitter_ms: float = 0.5,
    seed: int | None = 42,
) -> SimulationResult:
    """Approximate control-plane RTT using weighted shortest paths."""
    controller_list = list(controllers)
    if not controller_list:
        raise ValueError("controllers must not be empty")

    rng = random.Random(seed)
    distances = nx.multi_source_dijkstra_path_length(graph, controller_list, weight="weight")

    per_node: dict[str, float] = {}
    for node in graph.nodes:
        hop_distance = distances.get(node, float("inf"))
        if hop_distance == float("inf"):
            per_node[str(node)] = float("inf")
            continue
        jitter = rng.uniform(-jitter_ms, jitter_ms)
        per_node[str(node)] = max(0.0, hop_distance * base_link_delay_ms + jitter)

    finite_values = [value for value in per_node.values() if np.isfinite(value)]
    average_rtt = float(np.mean(finite_values)) if finite_values else float("inf")
    worst_rtt = float(np.max(finite_values)) if finite_values else float("inf")
    return SimulationResult(average_rtt_ms=average_rtt, worst_rtt_ms=worst_rtt, per_node_latency_ms=per_node)


def _run_mininet_latency_simulation(
    graph: nx.Graph,
    controllers: list[str],
    base_link_delay_ms: float,
    ping_count: int,
    timeout_s: int,
) -> SimulationResult:
    """Build a Mininet topology from the graph and measure host RTTs."""
    try:
        TCLink = import_module("mininet.link").TCLink
        Mininet = import_module("mininet.net").Mininet
        OVSSwitch = import_module("mininet.node").OVSSwitch
        Topo = import_module("mininet.topo").Topo
    except Exception as exc:  # pragma: no cover - depends on host environment
        raise RuntimeError("Mininet is unavailable in this environment") from exc

    node_labels = [str(node) for node in graph.nodes]
    node_to_index = {node: idx for idx, node in enumerate(node_labels, start=1)}

    class GraphTopo(Topo):
        def build(self):
            for node in node_labels:
                idx = node_to_index[node]
                switch_name = f"s{idx}"
                host_name = f"h{idx}"
                self.addSwitch(switch_name, failMode="standalone")
                self.addHost(host_name)
                self.addLink(host_name, switch_name, cls=TCLink, delay="0.10ms")

            for u, v, data in graph.edges(data=True):
                delay_ms = max(0.10, float(data.get("weight", 1.0)) * base_link_delay_ms)
                self.addLink(
                    f"s{node_to_index[str(u)]}",
                    f"s{node_to_index[str(v)]}",
                    cls=TCLink,
                    delay=f"{delay_ms:.2f}ms",
                )

    net = Mininet(
        topo=GraphTopo(),
        switch=OVSSwitch,
        controller=None,
        autoSetMacs=True,
        build=False,
    )

    try:
        net.build()
        net.start()

        host_by_node = {
            node: net.get(f"h{node_to_index[node]}")
            for node in node_labels
        }

        missing_controllers = [controller for controller in controllers if controller not in host_by_node]
        if missing_controllers:
            raise ValueError(f"Controller nodes not found in graph: {missing_controllers}")

        per_node: dict[str, float] = {}
        for node in node_labels:
            if node in controllers:
                per_node[node] = 0.0
                continue

            src_host = host_by_node[node]
            best_rtt = float("inf")

            for controller in controllers:
                dst_host = host_by_node[controller]
                ping_output = src_host.cmd(
                    f"ping -c {ping_count} -W {timeout_s} {dst_host.IP()}"
                )
                avg_rtt = _parse_ping_avg_ms(ping_output)
                if avg_rtt is None:
                    continue
                best_rtt = min(best_rtt, avg_rtt)

            per_node[node] = best_rtt

        finite_values = [value for value in per_node.values() if np.isfinite(value)]
        average_rtt = float(np.mean(finite_values)) if finite_values else float("inf")
        worst_rtt = float(np.max(finite_values)) if finite_values else float("inf")
        return SimulationResult(
            average_rtt_ms=average_rtt,
            worst_rtt_ms=worst_rtt,
            per_node_latency_ms=per_node,
        )
    finally:  # pragma: no cover - depends on host environment
        try:
            net.stop()
        except Exception:
            pass


def run_mininet_simulation(
    graph: nx.Graph,
    controllers: Iterable[str],
    base_link_delay_ms: float = 2.0,
    jitter_ms: float = 0.5,
    seed: int | None = 42,
    ping_count: int = 2,
    timeout_s: int = 1,
    fallback_to_synthetic: bool = True,
) -> SimulationResult:
    """
    Run Mininet-backed RTT simulation.

    Falls back to synthetic latency simulation if Mininet is unavailable or execution fails,
    unless fallback_to_synthetic is False.
    """
    controller_list = [str(controller) for controller in controllers]
    if not controller_list:
        raise ValueError("controllers must not be empty")

    try:
        return _run_mininet_latency_simulation(
            graph=graph,
            controllers=controller_list,
            base_link_delay_ms=base_link_delay_ms,
            ping_count=ping_count,
            timeout_s=timeout_s,
        )
    except (Exception, SystemExit, BaseException) as exc:
        if not fallback_to_synthetic:
            raise

        warnings.warn(
            f"Mininet simulation unavailable ({exc}). Falling back to synthetic simulation.",
            RuntimeWarning,
            stacklevel=2,
        )
        return run_synthetic_latency_simulation(
            graph=graph,
            controllers=controller_list,
            base_link_delay_ms=base_link_delay_ms,
            jitter_ms=jitter_ms,
            seed=seed,
        )

```

### `scripts/train_dqn_pilot.py`
```
#!/usr/bin/env python3
"""
Section 8.4.4: DQN Pilot Training Loop
========================================

Deep Q-Network training on Internet2 canonical topology.
Implements the Technical Stack Defense hyperparameters from Section 8.4.1:
  - learning_rate: 0.001
  - batch_size: 32
  - gamma: 0.99
  - max_episodes: 1000 (pilot uses 50)
  - replay_memory: 10,000

Validates end-to-end pipeline: proposal → config → topology → DQN training → metrics.json
"""

import json
import random
import sys
import time
from collections import deque
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from topology.canonical_topologies import load_canonical_topology


# ============================================================================
# Configuration Loading (Section 8.4.1 → Code)
# ============================================================================

def load_config() -> Dict:
    """Load experiment configuration from experiment_config.json."""
    config_path = Path(__file__).parent.parent / "configs" / "experiment_config.json"
    with open(config_path, "r") as f:
        return json.load(f)


CONFIG = load_config()
RL_CONFIG = CONFIG.get("rl_hyperparameters", {})

LEARNING_RATE = RL_CONFIG.get("learning_rate", 0.001)
BATCH_SIZE = RL_CONFIG.get("batch_size", 32)
GAMMA = RL_CONFIG.get("gamma", 0.99)
REPLAY_MEMORY_SIZE = RL_CONFIG.get("replay_memory_size", 10000)
TARGET_UPDATE_FREQ = RL_CONFIG.get("target_update_frequency", 100)
EPSILON_START = RL_CONFIG.get("epsilon_start", 1.0)
EPSILON_END = RL_CONFIG.get("epsilon_end", 0.05)
EPSILON_DECAY = RL_CONFIG.get("epsilon_decay", 0.995)

# Pilot / Training constants
PILOT_EPISODES = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else RL_CONFIG.get("max_episodes", 1000)
DEVICE = torch.device("cpu")


# ============================================================================
# Network Architecture
# ============================================================================

class DQNetwork(nn.Module):
    """
    Deep Q-Network with 2 hidden layers (64 neurons each).
    Input: state (node encoding)
    Output: Q-values for each action (controller placement)
    """

    def __init__(self, input_size: int, output_size: int):
        super().__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_size)
        self.relu = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through network."""
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# ============================================================================
# Replay Buffer
# ============================================================================

class ReplayBuffer:
    """Experience replay buffer (size: 10,000 from Farahi spec)."""

    def __init__(self, capacity: int = 10000):
        self.buffer = deque(maxlen=capacity)
        self.capacity = capacity

    def push(self, state, action, reward, next_state, done):
        """Add experience to buffer."""
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int) -> Tuple:
        """Sample random batch from buffer."""
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.tensor(states, dtype=torch.float32, device=DEVICE),
            torch.tensor(actions, dtype=torch.int64, device=DEVICE),
            torch.tensor(rewards, dtype=torch.float32, device=DEVICE),
            torch.tensor(next_states, dtype=torch.float32, device=DEVICE),
            torch.tensor(dones, dtype=torch.float32, device=DEVICE),
        )

    def __len__(self):
        return len(self.buffer)


# ============================================================================
# Environment: Controller Placement on Internet2
# ============================================================================

class ControllerPlacementEnv:
    """
    Simple environment for controller placement on Internet2.
    State: one-hot encoding of current controller position
    Action: place controller on a specific node
    Reward: based on latency and reliability
    """

    def __init__(self, graph, k: int = 3, use_weighted_paths: bool = True):
        self.graph = graph
        self.num_nodes = graph.number_of_nodes()
        self.nodes = list(graph.nodes())
        self.k = max(1, min(k, self.num_nodes))
        self.use_weighted_paths = use_weighted_paths
        
        # Pre-compute latency baseline
        self.max_latency = self._compute_max_avg_distance()
        
        # Tracking
        self.current_controller = None
        self.current_controllers: List[str] = []
        self.step_count = 0
        self.episode_rewards = []

    def _compute_max_avg_distance(self) -> float:
        """Compute worst-case average distance for normalization."""
        import networkx as nx
        max_avg = 0.0
        for node in self.graph.nodes():
            if self.use_weighted_paths:
                lengths = nx.single_source_dijkstra_path_length(self.graph, node, weight="weight")
            else:
                lengths = nx.single_source_shortest_path_length(self.graph, node)
            avg_dist = np.mean(list(lengths.values())) if lengths else 0.0
            max_avg = max(max_avg, avg_dist)
        return max_avg if max_avg > 0 else 1.0

    def _compute_latency(self, controller_node) -> float:
        """
        Compute average latency: mean shortest path from controller(s) to all nodes.
        Normalized by max_latency.
        """
        import networkx as nx
        sources = controller_node if isinstance(controller_node, (list, tuple, set)) else [controller_node]
        if self.use_weighted_paths:
            lengths = nx.multi_source_dijkstra_path_length(self.graph, list(sources), weight="weight")
        else:
            lengths = nx.multi_source_dijkstra_path_length(self.graph, list(sources), weight=None)
        avg_dist = np.mean(list(lengths.values())) if lengths else 0.0
        return avg_dist / self.max_latency

    def _compute_reliability(self, controller_node) -> float:
        """
        Compute N-1 single-link failure reachability from controller(s).
        """
        from evaluation.metrics import control_plane_reliability_single_link_failure_cached
        sources = controller_node if isinstance(controller_node, (list, tuple, set)) else [controller_node]
        return control_plane_reliability_single_link_failure_cached(self.graph, list(sources))

    def reset(self) -> np.ndarray:
        """Reset environment and return initial state."""
        self.current_controllers = random.sample(self.nodes, self.k)
        self.current_controller = self.current_controllers[0]
        self.step_count = 0
        self.episode_rewards = []
        return self._state_to_vector()

    def _state_to_vector(self) -> np.ndarray:
        """Convert controller node(s) to multi-hot state vector."""
        state = np.zeros(self.num_nodes, dtype=np.float32)
        active = self.current_controllers if self.current_controllers else [self.current_controller]
        for ctrl in active:
            if ctrl in self.nodes:
                state[self.nodes.index(ctrl)] = 1.0
        return state

    def step(self, action: int) -> Tuple[np.ndarray, float, bool]:
        """
        Execute action (update controller placement).
        Return: (next_state, reward, done)
        """
        self.step_count += 1
        
        # Action: select controller node and maintain k-controller active set
        if 0 <= action < self.num_nodes:
            selected = self.nodes[action]
            self.current_controller = selected
            if selected not in self.current_controllers:
                if len(self.current_controllers) >= self.k:
                    self.current_controllers.pop(0)
                self.current_controllers.append(selected)
        
        # Compute metrics across the active k-controller placement
        active_set = self.current_controllers if self.current_controllers else [self.current_controller]
        latency = self._compute_latency(active_set)
        reliability = self._compute_reliability(active_set)
        
        # Reward logic (Section 8.4.1 specifications)
        latency_score = -(latency)  # Negative latency is good
        reliability_score = reliability * 2  # Amplified reliability reward
        penalty = -10.0 if reliability < 0.8 else 0.0  # Harsh penalty for low reliability
        
        reward = latency_score + reliability_score + penalty
        
        # Episode terminates after fixed steps (proof of concept)
        done = self.step_count >= 10
        
        self.episode_rewards.append(reward)
        next_state = self._state_to_vector()
        
        return next_state, reward, done


# ============================================================================
# DQN Agent
# ============================================================================

class DQNAgent:
    """Deep Q-Network agent for controller placement."""

    def __init__(self, state_size: int, action_size: int):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = EPSILON_START
        
        # Networks
        self.q_network = DQNetwork(state_size, action_size).to(DEVICE)
        self.target_network = DQNetwork(state_size, action_size).to(DEVICE)
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Optimizer
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=LEARNING_RATE)
        
        # Replay buffer
        self.memory = ReplayBuffer(REPLAY_MEMORY_SIZE)
        
        # Tracking
        self.update_count = 0

    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay buffer."""
        self.memory.push(state, action, reward, next_state, done)

    def act(self, state: np.ndarray) -> int:
        """Epsilon-greedy action selection."""
        if np.random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        
        state_tensor = torch.tensor(state, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        with torch.no_grad():
            q_values = self.q_network(state_tensor)
        return q_values.argmax(dim=1).item()

    def replay(self, batch_size: int):
        """Train on batch from replay buffer."""
        if len(self.memory) < batch_size:
            return
        
        states, actions, rewards, next_states, dones = self.memory.sample(batch_size)
        
        # Current Q-values
        q_values = self.q_network(states)
        q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        
        # Target Q-values
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(dim=1)[0]
            target_q_values = rewards + (1 - dones) * GAMMA * next_q_values
        
        # Loss
        loss = nn.MSELoss()(q_values, target_q_values)
        
        # Backprop
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Update target network periodically
        self.update_count += 1
        if self.update_count % TARGET_UPDATE_FREQ == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
        
        return loss.item()

    def decay_epsilon(self):
        """Decay exploration rate."""
        self.epsilon = max(EPSILON_END, self.epsilon * EPSILON_DECAY)


# ============================================================================
# Training Loop
# ============================================================================

def train_pilot():
    """Run pilot DQN training (50 episodes)."""
    print("\n" + "=" * 70)
    print("DQN PILOT TRAINING (Section 8.4.4)")
    print("=" * 70)
    
    # Load topology
    print("\n[1/4] Loading Internet2 topology...")
    G = load_canonical_topology("Internet2", seed=42)
    print(f"  ✓ Loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Create environment and agent
    print("\n[2/4] Initializing environment and agent...")
    env = ControllerPlacementEnv(G, k=3, use_weighted_paths=True)
    agent = DQNAgent(state_size=G.number_of_nodes(), action_size=G.number_of_nodes())
    print(f"  ✓ DQN Network: Input({G.number_of_nodes()}) -> Hidden(64) -> Hidden(64) -> Output({G.number_of_nodes()})")
    print(f"  ✓ Replay Buffer: {REPLAY_MEMORY_SIZE} capacity")
    print(f"  ✓ Hyperparameters: LR={LEARNING_RATE}, γ={GAMMA}, batch={BATCH_SIZE}")
    
    # Training loop
    print(f"\n[3/4] Training for {PILOT_EPISODES} episodes...")
    episode_rewards = []
    start_time = time.time()
    
    for episode in range(PILOT_EPISODES):
        state = env.reset()
        episode_reward = 0
        done = False
        
        while not done:
            # Agent selects action
            action = agent.act(state)
            
            # Environment step
            next_state, reward, done = env.step(action)
            episode_reward += reward
            
            # Store in replay buffer
            agent.remember(state, action, reward, next_state, done)
            
            # Train on batch
            if len(agent.memory) >= BATCH_SIZE:
                agent.replay(BATCH_SIZE)
            
            state = next_state
        
        # Decay exploration
        agent.decay_epsilon()
        episode_rewards.append(episode_reward)
        
        # Progress
        if (episode + 1) % 10 == 0:
            avg_reward = np.mean(episode_rewards[-10:])
            print(f"  Episode {episode + 1:3d}/{PILOT_EPISODES}: avg_reward={avg_reward:8.3f}, ε={agent.epsilon:.3f}")
    
    elapsed = time.time() - start_time
    
    # Summary
    print("\n[4/4] Pilot training complete!")
    print(f"  ✓ Elapsed time: {elapsed:.1f}s ({elapsed/PILOT_EPISODES:.2f}s/episode)")
    print(f"  ✓ Final avg reward: {np.mean(episode_rewards[-10:]):.3f}")
    print(f"  ✓ Best episode: {max(episode_rewards):.3f}")
    print(f"  ✓ Worst episode: {min(episode_rewards):.3f}")
    
    # Save metrics
    print("\n[EXPORTING] Writing pilot_metrics.json...")
    output_path = Path(__file__).parent.parent / "results" / "pilot_metrics.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    metrics = {
        "metadata": {
            "pilot_episodes": PILOT_EPISODES,
            "total_steps": sum(env.step_count for _ in range(PILOT_EPISODES)),
            "elapsed_seconds": elapsed,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "hyperparameters": {
            "learning_rate": LEARNING_RATE,
            "batch_size": BATCH_SIZE,
            "gamma": GAMMA,
            "replay_memory_size": REPLAY_MEMORY_SIZE,
            "target_update_frequency": TARGET_UPDATE_FREQ,
            "epsilon_start": EPSILON_START,
            "epsilon_end": EPSILON_END,
            "epsilon_decay": EPSILON_DECAY
        },
        "topology": {
            "name": "Internet2",
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "seed": 42
        },
        "episode_rewards": episode_rewards,
        "statistics": {
            "mean_reward": float(np.mean(episode_rewards)),
            "std_reward": float(np.std(episode_rewards)),
            "max_reward": float(np.max(episode_rewards)),
            "min_reward": float(np.min(episode_rewards)),
            "final_10_episode_avg": float(np.mean(episode_rewards[-10:]))
        }
    }
    
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"  ✓ Metrics saved: {output_path}")
    print("\n" + "=" * 70)
    print("PILOT RUN SUCCESSFUL")
    print("=" * 70 + "\n")
    
    return metrics


if __name__ == "__main__":
    metrics = train_pilot()

```

### `scripts/run_stability_audit.py`
```
#!/usr/bin/env python3
"""
Phase 5 Stability Audit Protocol

Runs fixed-hyperparameter DQN stability experiments over:
  - Topologies: Internet2, ATT-MPLS
  - Seeds: [42, 123, 256, 512, 1024]
  - Episodes: 1000

Outputs:
  - Episode logs (JSONL)
  - Run summaries (CSV + JSON)

This script is graph-only by design (Phase 5), with no Mininet dependency.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

PROJECT_ROOT = Path(__file__).resolve().parents[1]

import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.metrics import (  # noqa: E402
    average_controller_distance,
    control_plane_reliability_single_link_failure_cached,
    precompute_reliability_cache,
)
from topology.canonical_topologies import load_canonical_topology  # noqa: E402


FIXED_SEEDS = [42, 123, 256, 512, 1024]
FIXED_TOPOLOGIES = ["Internet2", "ATT-MPLS"]


@dataclass
class RunSummary:
    topology: str
    seed: int
    episodes: int
    learning_rate: float
    batch_size: int
    gamma: float
    rolling_mean_reward_last100: float
    reward_variance_last200: float
    final_best_reward: float
    final_epsilon: float
    normalized_action_entropy: float
    final_latency: float
    final_reliability: float
    final_omega_ms_per_episode: float
    divergence_flag: bool
    divergence_reason: str


class DQNetwork(nn.Module):
    def __init__(self, input_size: int, output_size: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_size),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buffer: deque = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int, device: torch.device):
        batch_size = min(batch_size, len(self.buffer))
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.tensor(np.array(states), dtype=torch.float32, device=device),
            torch.tensor(actions, dtype=torch.int64, device=device),
            torch.tensor(rewards, dtype=torch.float32, device=device),
            torch.tensor(np.array(next_states), dtype=torch.float32, device=device),
            torch.tensor(dones, dtype=torch.float32, device=device),
        )

    def __len__(self) -> int:
        return len(self.buffer)


class GraphPlacementEnv:
    def __init__(self, graph):
        self.graph = graph
        self.nodes = [str(n) for n in graph.nodes()]
        self.num_nodes = len(self.nodes)
        self.controller = self.nodes[0]
        self.steps = 0
        self.max_steps = 10

        self.max_latency = self._max_latency_baseline()
        precompute_reliability_cache(graph)

    def _max_latency_baseline(self) -> float:
        latencies = []
        for node in self.nodes:
            latencies.append(average_controller_distance(self.graph, [node]))
        finite = [v for v in latencies if np.isfinite(v)]
        return max(finite) if finite else 1.0

    def reset(self, rng: random.Random) -> np.ndarray:
        self.controller = rng.choice(self.nodes)
        self.steps = 0
        return self._state()

    def _state(self) -> np.ndarray:
        vec = np.zeros(self.num_nodes, dtype=np.float32)
        vec[self.nodes.index(self.controller)] = 1.0
        return vec

    def step(self, action_idx: int) -> tuple[np.ndarray, float, bool, dict[str, float]]:
        self.steps += 1
        if 0 <= action_idx < self.num_nodes:
            self.controller = self.nodes[action_idx]

        latency = average_controller_distance(self.graph, [self.controller])
        latency_norm = latency / max(self.max_latency, 1e-9)
        reliability = control_plane_reliability_single_link_failure_cached(self.graph, [self.controller])

        # Reward aligns with study objective: minimize latency, maximize reliability.
        reward = -(latency_norm) + (2.0 * reliability) - (10.0 if reliability < 0.8 else 0.0)

        done = self.steps >= self.max_steps
        return self._state(), float(reward), done, {
            "latency": float(latency),
            "reliability": float(reliability),
        }


def _normalized_entropy(action_counts: np.ndarray) -> float:
    total = float(np.sum(action_counts))
    if total <= 0:
        return 0.0
    probs = action_counts / total
    probs = probs[probs > 0]
    if probs.size == 0:
        return 0.0
    entropy = -np.sum(probs * np.log2(probs))
    max_entropy = math.log2(len(action_counts)) if len(action_counts) > 1 else 1.0
    return float(entropy / max(max_entropy, 1e-9))


def _rolling_mean(values: list[float], window: int) -> float:
    if not values:
        return 0.0
    arr = np.array(values[-window:], dtype=np.float64)
    return float(arr.mean())


def run_single_stability_audit(
    topology_name: str,
    seed: int,
    episodes: int,
    learning_rate: float,
    batch_size: int,
    gamma: float,
    replay_memory_size: int,
    target_update_frequency: int,
    epsilon_start: float,
    epsilon_end: float,
    epsilon_decay: float,
    event_log_path: Path,
) -> RunSummary:
    torch.manual_seed(seed)
    np.random.seed(seed)
    rng = random.Random(seed)

    graph = load_canonical_topology(topology_name, seed=seed)
    env = GraphPlacementEnv(graph)

    device = torch.device("cpu")
    state_size = env.num_nodes
    action_size = env.num_nodes

    q_net = DQNetwork(state_size, action_size).to(device)
    target_net = DQNetwork(state_size, action_size).to(device)
    target_net.load_state_dict(q_net.state_dict())
    optimizer = optim.Adam(q_net.parameters(), lr=learning_rate)

    memory = ReplayBuffer(replay_memory_size)
    epsilon = epsilon_start

    best_reward = float("-inf")
    episode_rewards: list[float] = []
    action_counts = np.zeros(action_size, dtype=np.int64)
    last_latency = float("inf")
    last_reliability = 0.0

    event_log_path.parent.mkdir(parents=True, exist_ok=True)
    run_start = time.perf_counter()
    with event_log_path.open("a", encoding="utf-8") as event_log:
        for episode in range(1, episodes + 1):
            state = env.reset(rng)
            ep_reward = 0.0

            for _ in range(env.max_steps):
                if rng.random() < epsilon:
                    action = rng.randint(0, action_size - 1)
                else:
                    with torch.no_grad():
                        qvals = q_net(torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0))
                        action = int(torch.argmax(qvals, dim=1).item())

                action_counts[action] += 1

                next_state, reward, done, info = env.step(action)
                ep_reward += reward
                last_latency = info["latency"]
                last_reliability = info["reliability"]

                memory.push(state, action, reward, next_state, done)
                state = next_state

                if len(memory) >= batch_size:
                    s, a, r, ns, d = memory.sample(batch_size, device)
                    q_values = q_net(s).gather(1, a.unsqueeze(1)).squeeze(1)
                    with torch.no_grad():
                        next_q = target_net(ns).max(dim=1)[0]
                        target = r + (1.0 - d) * gamma * next_q
                    loss = nn.MSELoss()(q_values, target)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                if done:
                    break

            episode_rewards.append(float(ep_reward))
            best_reward = max(best_reward, ep_reward)
            epsilon = max(epsilon_end, epsilon * epsilon_decay)

            if episode % target_update_frequency == 0:
                target_net.load_state_dict(q_net.state_dict())

            if episode == 1 or episode % 25 == 0 or episode == episodes:
                record = {
                    "event": "episode",
                    "topology": topology_name,
                    "seed": seed,
                    "episode": episode,
                    "reward": float(ep_reward),
                    "rolling_mean_50": _rolling_mean(episode_rewards, 50),
                    "best_reward": float(best_reward),
                    "epsilon": float(epsilon),
                    "action_entropy": _normalized_entropy(action_counts),
                    "latency": float(last_latency),
                    "reliability": float(last_reliability),
                }
                event_log.write(json.dumps(record, sort_keys=True) + "\n")

    reward_arr = np.array(episode_rewards, dtype=np.float64)
    reward_var_last200 = float(np.var(reward_arr[-200:])) if reward_arr.size else float("inf")
    rolling_last100 = _rolling_mean(episode_rewards, 100)
    entropy = _normalized_entropy(action_counts)

    divergence_flag = False
    divergence_reason = "stable"
    if np.isnan(reward_arr).any() or np.isinf(reward_arr).any():
        divergence_flag = True
        divergence_reason = "nan_or_inf_reward"
    elif reward_var_last200 > 50.0:
        divergence_flag = True
        divergence_reason = "high_reward_variance_last200"
    elif rolling_last100 < -50.0:
        divergence_flag = True
        divergence_reason = "reward_collapse_last100"

    run_elapsed_s = time.perf_counter() - run_start
    omega_ms = float((run_elapsed_s / max(episodes, 1)) * 1000.0)

    return RunSummary(
        topology=topology_name,
        seed=seed,
        episodes=episodes,
        learning_rate=learning_rate,
        batch_size=batch_size,
        gamma=gamma,
        rolling_mean_reward_last100=rolling_last100,
        reward_variance_last200=reward_var_last200,
        final_best_reward=float(best_reward),
        final_epsilon=float(epsilon),
        normalized_action_entropy=entropy,
        final_latency=float(last_latency),
        final_reliability=float(last_reliability),
        final_omega_ms_per_episode=omega_ms,
        divergence_flag=divergence_flag,
        divergence_reason=divergence_reason,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run 5-seed DQN stability audit across canonical topologies")
    parser.add_argument("--episodes", type=int, default=1000, help="Episodes per run (default: 1000)")
    parser.add_argument(
        "--topologies",
        type=str,
        default=",".join(FIXED_TOPOLOGIES),
        help="Comma-separated topology names (default: Internet2,ATT-MPLS)",
    )
    parser.add_argument(
        "--seeds",
        type=str,
        default=",".join(str(seed) for seed in FIXED_SEEDS),
        help="Comma-separated fixed seeds",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(PROJECT_ROOT / "results" / "rl_analysis" / "stability_audit"),
        help="Output directory for summaries/logs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    config_path = PROJECT_ROOT / "configs" / "experiment_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    hp = config.get("rl_hyperparameters", {})

    # Enforce fixed Farahi parameters.
    learning_rate = 0.001
    batch_size = 32
    gamma = 0.99

    replay_memory_size = int(hp.get("replay_memory_size", 10000))
    target_update_frequency = int(hp.get("target_update_frequency", 100))
    epsilon_start = float(hp.get("epsilon_start", 1.0))
    epsilon_end = float(hp.get("epsilon_end", 0.05))
    epsilon_decay = float(hp.get("epsilon_decay", 0.995))

    topologies = [name.strip() for name in args.topologies.split(",") if name.strip()]
    seeds = [int(value.strip()) for value in args.seeds.split(",") if value.strip()]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    event_log_path = output_dir / "training_events.jsonl"
    if event_log_path.exists():
        event_log_path.unlink()

    summaries: list[RunSummary] = []
    for topology_name in topologies:
        for seed in seeds:
            summary = run_single_stability_audit(
                topology_name=topology_name,
                seed=seed,
                episodes=args.episodes,
                learning_rate=learning_rate,
                batch_size=batch_size,
                gamma=gamma,
                replay_memory_size=replay_memory_size,
                target_update_frequency=target_update_frequency,
                epsilon_start=epsilon_start,
                epsilon_end=epsilon_end,
                epsilon_decay=epsilon_decay,
                event_log_path=event_log_path,
            )
            summaries.append(summary)
            print(
                f"[done] topology={summary.topology} seed={summary.seed} "
                f"best={summary.final_best_reward:.4f} entropy={summary.normalized_action_entropy:.4f} "
                f"divergence={summary.divergence_flag}"
            )

    summary_records = [asdict(item) for item in summaries]
    summary_df = pd.DataFrame(summary_records)

    summary_csv = output_dir / "stability_summary.csv"
    summary_json = output_dir / "stability_summary.json"
    grouped_csv = output_dir / "stability_grouped_by_topology.csv"

    summary_df.to_csv(summary_csv, index=False)
    summary_json.write_text(json.dumps(summary_records, indent=2), encoding="utf-8")

    grouped = (
        summary_df.groupby("topology")
        .agg(
            runs=("seed", "count"),
            mean_best_reward=("final_best_reward", "mean"),
            std_best_reward=("final_best_reward", "std"),
            mean_entropy=("normalized_action_entropy", "mean"),
            mean_rolling_reward_last100=("rolling_mean_reward_last100", "mean"),
            mean_latency=("final_latency", "mean"),
            mean_reliability=("final_reliability", "mean"),
            divergence_runs=("divergence_flag", "sum"),
        )
        .reset_index()
    )
    grouped.to_csv(grouped_csv, index=False)

    print("\n=== Stability Audit Completed ===")
    print(f"Summary CSV: {summary_csv}")
    print(f"Summary JSON: {summary_json}")
    print(f"Grouped CSV: {grouped_csv}")
    print(f"Episode log: {event_log_path}")


if __name__ == "__main__":
    main()

```

### `tests/test_rl_logging.py`
```
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import networkx as nx

from algorithms.ai.reinforcement_learning import (
    bandit_rl_controller_placement,
    dqn_controller_placement,
)


class ReinforcementLearningLoggingTests(unittest.TestCase):
    def test_bandit_rl_writes_jsonl_trace(self) -> None:
        graph = nx.path_graph([f"n{i}" for i in range(6)])

        latency_weight = 1.5
        reliability_weight = 0.75

        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "logs" / "rl_training.jsonl"

            placement = bandit_rl_controller_placement(
                graph=graph,
                num_controllers=2,
                episodes=10,
                epsilon=0.2,
                candidate_pool_size=16,
                seed=7,
                log_path=str(log_path),
                log_every=3,
                run_label="unit_test",
                latency_weight=latency_weight,
                reliability_weight=reliability_weight,
            )

            self.assertEqual(len(placement), 2)
            self.assertEqual(len(set(placement)), 2)
            self.assertTrue(log_path.exists())

            records = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]

        self.assertGreaterEqual(len(records), 3)
        self.assertEqual(records[0]["event"], "run_start")
        self.assertEqual(records[-1]["event"], "run_end")

        run_ids = {record["run_id"] for record in records}
        self.assertEqual(len(run_ids), 1)

        episode_records = [record for record in records if record["event"] == "episode"]
        self.assertEqual([record["episode"] for record in episode_records], [1, 3, 6, 9, 10])

        self.assertIn("num_actions", records[0])
        self.assertIn("epsilon_start", records[0])
        self.assertEqual(records[0]["latency_weight"], latency_weight)
        self.assertEqual(records[0]["reliability_weight"], reliability_weight)

        # Reward should match the configured composite objective formula.
        first_episode = episode_records[0]
        expected_reward = (
            -(latency_weight * float(first_episode["selected_action_avg_distance"]))
            + (reliability_weight * float(first_episode["selected_action_reliability"]))
        )
        self.assertAlmostEqual(float(first_episode["reward"]), expected_reward, places=10)

        self.assertIn("best_action", records[-1])
        self.assertIn("top_actions", records[-1])
        self.assertTrue(records[-1]["top_actions"])

    def test_log_every_must_be_positive(self) -> None:
        graph = nx.path_graph(["a", "b", "c"])

        with self.assertRaises(ValueError):
            bandit_rl_controller_placement(
                graph=graph,
                num_controllers=1,
                episodes=5,
                log_path="unused.jsonl",
                log_every=0,
            )

    def test_negative_weights_are_rejected(self) -> None:
        graph = nx.path_graph(["a", "b", "c"])

        with self.assertRaises(ValueError):
            bandit_rl_controller_placement(
                graph=graph,
                num_controllers=1,
                latency_weight=-1.0,
            )

        with self.assertRaises(ValueError):
            bandit_rl_controller_placement(
                graph=graph,
                num_controllers=1,
                reliability_weight=-0.1,
            )

    def test_dqn_controller_placement_returns_metadata_and_timing(self) -> None:
        graph = nx.barabasi_albert_graph(10, 2, seed=42)
        mapping = {i: f"n{i}" for i in graph.nodes}
        graph = nx.relabel_nodes(graph, mapping)
        for u, v in graph.edges:
            graph[u][v]["weight"] = 1.0

        controllers, meta = dqn_controller_placement(
            graph=graph,
            num_controllers=2,
            episodes=10,
            seed=42,
            return_metadata=True,
        )
        self.assertEqual(len(controllers), 2)
        self.assertEqual(len(set(controllers)), 2)
        self.assertIn("training_time_sec", meta)
        self.assertIn("inference_time_ms", meta)
        self.assertGreater(meta["training_time_sec"], 0.0)
        self.assertGreater(meta["inference_time_ms"], 0.0)


if __name__ == "__main__":
    unittest.main()

```

### `results/experiment_data/complete_proposal_aligned_benchmark.csv`
```
Topology,Nodes (N),Edges (E),Budget (k),Algorithm,Avg Latency (ms),N-1 Reliability (%),Runtime (ms),Inference (ms),Complexity Tax ω (s/ep),Controllers
Internet2 (Canonical),20,26,3,K-Means,1.469,100.0,4.084,4.084,0.0041,n1; n16; n9
Internet2 (Canonical),20,26,3,Greedy K-Center,1.511,100.0,0.053,0.053,0.0001,n1; n10; n6
Internet2 (Canonical),20,26,3,Genetic Algorithm,1.403,100.0,12.878,12.878,0.0129,n1; n15; n16
Internet2 (Canonical),20,26,3,Bandit RL,1.564,100.0,72.054,0.029,0.0213,n1; n10; n5
Internet2 (Canonical),20,26,3,Random Baseline,1.734,100.0,0.007,0.007,0.0,n13; n0; n18
Internet2 (Canonical),20,26,5,K-Means,1.045,100.0,4.983,4.983,0.005,n10; n2; n4; n6; n9
Internet2 (Canonical),20,26,5,Greedy K-Center,1.064,100.0,0.095,0.095,0.0001,n1; n10; n6; n13; n8
Internet2 (Canonical),20,26,5,Genetic Algorithm,0.976,100.0,20.532,20.532,0.0205,n17; n18; n2; n4; n6
Internet2 (Canonical),20,26,5,Bandit RL,0.96,100.0,73.147,0.029,0.0213,n1; n10; n15; n16; n4
Internet2 (Canonical),20,26,5,Random Baseline,1.277,100.0,0.009,0.009,0.0,n13; n0; n18; n17; n8
ATT-MPLS (Canonical),21,54,3,K-Means,2.391,100.0,4.144,4.144,0.0041,4; 8; 10
ATT-MPLS (Canonical),21,54,3,Greedy K-Center,3.03,100.0,0.081,0.081,0.0001,5; 2; 13
ATT-MPLS (Canonical),21,54,3,Genetic Algorithm,2.32,100.0,15.853,15.853,0.0159,1; 4; 7
ATT-MPLS (Canonical),21,54,3,Bandit RL,2.37,100.0,273.058,0.021,0.0213,4; 7; 8
ATT-MPLS (Canonical),21,54,3,Random Baseline,3.289,100.0,0.01,0.01,0.0,20; 3; 0
ATT-MPLS (Canonical),21,54,5,K-Means,2.336,100.0,4.133,4.133,0.0041,11; 5; 19; 18; 12
ATT-MPLS (Canonical),21,54,5,Greedy K-Center,2.381,100.0,0.131,0.131,0.0001,5; 2; 13; 12; 18
ATT-MPLS (Canonical),21,54,5,Genetic Algorithm,1.828,100.0,20.288,20.288,0.0203,1; 4; 7; 13; 17
ATT-MPLS (Canonical),21,54,5,Bandit RL,1.923,100.0,251.254,0.021,0.0213,0; 1; 2; 7; 17
ATT-MPLS (Canonical),21,54,5,Random Baseline,2.177,100.0,0.007,0.007,0.0,20; 3; 0; 8; 7
Barabási-Albert (N=20),20,36,3,K-Means,7.042,100.0,3.781,3.781,0.0038,n15; n11; n10
Barabási-Albert (N=20),20,36,3,Greedy K-Center,5.528,100.0,0.06,0.06,0.0001,n0; n12; n16
Barabási-Albert (N=20),20,36,3,Genetic Algorithm,4.281,100.0,15.216,15.216,0.0152,n1; n4; n8
Barabási-Albert (N=20),20,36,3,Bandit RL,4.752,100.0,144.786,0.029,0.0213,n0; n1; n4
Barabási-Albert (N=20),20,36,3,Random Baseline,5.925,100.0,0.007,0.007,0.0,n3; n0; n8
Barabási-Albert (N=20),20,36,5,K-Means,4.706,100.0,4.137,4.137,0.0041,n10; n13; n5; n15; n2
Barabási-Albert (N=20),20,36,5,Greedy K-Center,3.673,100.0,0.103,0.103,0.0001,n0; n12; n16; n8; n6
Barabási-Albert (N=20),20,36,5,Genetic Algorithm,3.407,100.0,18.932,18.932,0.0189,n0; n1; n2; n5; n8
Barabási-Albert (N=20),20,36,5,Bandit RL,3.493,100.0,147.891,0.029,0.0213,n0; n1; n4; n5; n8
Barabási-Albert (N=20),20,36,5,Random Baseline,4.863,100.0,0.007,0.007,0.0,n3; n0; n8; n7; n16
Barabási-Albert (N=50),50,96,3,K-Means,6.514,100.0,4.382,4.382,0.0044,n49; n36; n6
Barabási-Albert (N=50),50,96,3,Greedy K-Center,5.412,100.0,0.089,0.089,0.0001,n0; n48; n37
Barabási-Albert (N=50),50,96,3,Genetic Algorithm,4.937,100.0,32.467,32.467,0.0325,n0; n16; n5
Barabási-Albert (N=50),50,96,3,Bandit RL,5.465,100.0,918.771,0.022,0.0213,n0; n1; n4
Barabási-Albert (N=50),50,96,3,Random Baseline,6.594,100.0,0.007,0.007,0.0,n40; n7; n1
Barabási-Albert (N=50),50,96,5,K-Means,6.398,100.0,4.871,4.871,0.0049,n10; n23; n2; n43; n7
Barabási-Albert (N=50),50,96,5,Greedy K-Center,4.691,100.0,0.165,0.165,0.0002,n0; n48; n37; n39; n35
Barabási-Albert (N=50),50,96,5,Genetic Algorithm,4.089,100.0,41.856,41.856,0.0419,n0; n15; n16; n29; n5
Barabási-Albert (N=50),50,96,5,Bandit RL,4.325,100.0,975.993,0.022,0.0213,n0; n1; n4; n5; n6
Barabási-Albert (N=50),50,96,5,Random Baseline,6.131,100.0,0.007,0.007,0.0,n40; n7; n1; n47; n17
Waxman (N=20),20,19,3,K-Means,2.73,94.47,3.193,3.193,0.0032,n2; n3; n1
Waxman (N=20),20,19,3,Greedy K-Center,4.935,97.37,0.037,0.037,0.0,n1; n17; n12
Waxman (N=20),20,19,3,Genetic Algorithm,2.64,96.05,13.15,13.15,0.0132,n1; n10; n8
Waxman (N=20),20,19,3,Bandit RL,2.73,94.47,52.345,0.029,0.0213,n1; n2; n3
Waxman (N=20),20,19,3,Random Baseline,4.609,96.05,0.007,0.007,0.0,n3; n0; n8
Waxman (N=20),20,19,5,K-Means,1.703,98.16,3.901,3.901,0.0039,n16; n9; n1; n18; n8
Waxman (N=20),20,19,5,Greedy K-Center,1.855,98.42,0.074,0.074,0.0001,n1; n17; n12; n16; n18
Waxman (N=20),20,19,5,Genetic Algorithm,1.494,96.84,16.307,16.307,0.0163,n1; n14; n15; n3; n5
Waxman (N=20),20,19,5,Bandit RL,1.603,97.89,49.738,0.029,0.0213,n1; n10; n17; n6; n9
Waxman (N=20),20,19,5,Random Baseline,2.695,96.32,0.007,0.007,0.0,n3; n0; n8; n7; n16
Waxman (N=50),50,53,3,K-Means,16.76,96.98,3.458,3.458,0.0035,n36; n2; n21
Waxman (N=50),50,53,3,Greedy K-Center,12.499,97.96,0.081,0.081,0.0001,n25; n38; n45
Waxman (N=50),50,53,3,Genetic Algorithm,7.707,97.58,28.321,28.321,0.0283,n1; n22; n48
Waxman (N=50),50,53,3,Bandit RL,8.721,98.19,388.416,0.022,0.0213,n14; n5; n6
Waxman (N=50),50,53,3,Random Baseline,16.296,95.51,0.011,0.011,0.0,n40; n7; n1
Waxman (N=50),50,53,5,K-Means,9.93,98.34,8.14,8.14,0.0081,n36; n5; n1; n26; n18
Waxman (N=50),50,53,5,Greedy K-Center,9.972,98.79,0.173,0.173,0.0002,n25; n38; n45; n26; n28
Waxman (N=50),50,53,5,Genetic Algorithm,5.468,98.34,39.026,39.026,0.039,n1; n14; n32; n37; n6
Waxman (N=50),50,53,5,Bandit RL,6.5,98.3,382.597,0.022,0.0213,n1; n14; n32; n35; n38
Waxman (N=50),50,53,5,Random Baseline,10.026,96.91,0.009,0.009,0.0,n40; n7; n1; n47; n17

```

### `results/mininet_overhead_validation.json`
```
{
  "test_date": "2026-05-20 00:41:47",
  "configuration": {
    "topology": "Internet2",
    "nodes": 11,
    "edges": 18,
    "controllers_per_trial": 3,
    "traffic_burst_duration": 0.2
  },
  "trials": 3,
  "threshold_ms": 2000,
  "exceeds_threshold": 3,
  "aggregate": {
    "phase_a_mean_ms": 662.275275021481,
    "phase_b_mean_ms": 137.68631600153944,
    "phase_c_mean_ms": 89.85504500257473,
    "phase_d_mean_ms": 1985.6765446796392,
    "online_loop_avg_ms": 889.8166360255951,
    "online_loop_min_ms": 869.6861080243252,
    "online_loop_max_ms": 913.1993459886871,
    "full_lifecycle_avg_ms": 2875.4931807052344,
    "full_lifecycle_min_ms": 2797.129835060332,
    "full_lifecycle_max_ms": 2974.6929109678604,
    "teardown_infrastructure_tax_avg_ms": 1985.6765446796392,
    "total_avg_ms": 2875.4931807052344,
    "total_min_ms": 2797.129835060332,
    "total_max_ms": 2974.6929109678604,
    "variability_ms": 177.5630759075284
  },
  "decision": "WARN",
  "recommendation": "3/3 trials exceeded 2000 ms threshold. Recommend deferring Mininet to Phase 6 validation on Pareto subset only. Phase 5: Use graph-based metrics (shortest-path latency, reachability). Phase 6: Validate top 5 Pareto solutions via Mininet.",
  "individual_trials": [
    {
      "phase_a_topo_instantiation": 695.8581079961732,
      "phase_b_controller_binding": 133.58916400466114,
      "phase_c_traffic_generation": 83.75207398785278,
      "phase_d_teardown": 2061.4935649791732,
      "online_loop_overhead_ms": 913.1993459886871,
      "full_lifecycle_overhead_ms": 2974.6929109678604
    },
    {
      "phase_a_topo_instantiation": 638.9789130189456,
      "phase_b_controller_binding": 138.16097303060815,
      "phase_c_traffic_generation": 92.54622197477147,
      "phase_d_teardown": 1927.4437270360067,
      "online_loop_overhead_ms": 869.6861080243252,
      "full_lifecycle_overhead_ms": 2797.129835060332
    },
    {
      "phase_a_topo_instantiation": 651.9888040493242,
      "phase_b_controller_binding": 141.308810969349,
      "phase_c_traffic_generation": 93.26683904509991,
      "phase_d_teardown": 1968.0923420237377,
      "online_loop_overhead_ms": 886.5644540637732,
      "full_lifecycle_overhead_ms": 2854.656796087511
    }
  ]
}
```

### `results/mininet_simulation_results.json`
```
{
  "Genetic Algorithm": {
    "placement": [
      "n1",
      "n15",
      "n16"
    ],
    "avg_rtt_ms": 2.718,
    "worst_rtt_ms": 6.903
  },
  "K-Means": {
    "placement": [
      "n1",
      "n16",
      "n9"
    ],
    "avg_rtt_ms": 2.852,
    "worst_rtt_ms": 5.764
  },
  "Greedy K-Center": {
    "placement": [
      "n1",
      "n10",
      "n6"
    ],
    "avg_rtt_ms": 2.934,
    "worst_rtt_ms": 6.664
  },
  "Bandit RL / DQN": {
    "placement": [
      "n1",
      "n10",
      "n5"
    ],
    "avg_rtt_ms": 3.056,
    "worst_rtt_ms": 6.718
  },
  "Random": {
    "placement": [
      "n13",
      "n0",
      "n18"
    ],
    "avg_rtt_ms": 3.374,
    "worst_rtt_ms": 6.944
  }
}
```
