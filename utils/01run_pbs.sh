#!/bin/bash
nohup bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/sedmail.sh &
      current_job_id=`qsub -V -N example_lncRNA.L13 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.L13.out -l nodes=1:ppn=8 -q batch <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/01runRNAseq_example_lncRNA_L13.sh' `
      job_ids="${job_ids}afterok:${current_job_id},"
      current_job_id=`qsub -V -N example_lncRNA.L15 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.L15.out -l nodes=1:ppn=8 -q batch <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/01runRNAseq_example_lncRNA_L15.sh' `
      job_ids="${job_ids}afterok:${current_job_id},"
      current_job_id=`qsub -V -N example_lncRNA.L17 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.L17.out -l nodes=1:ppn=8 -q batch <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/01runRNAseq_example_lncRNA_L17.sh' `
      job_ids="${job_ids}afterok:${current_job_id},"
      current_job_id=`qsub -V -N example_lncRNA.L19 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.L19.out -l nodes=1:ppn=8 -q batch <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/01runRNAseq_example_lncRNA_L19.sh' `
      job_ids="${job_ids}afterok:${current_job_id},"
      current_job_id=`qsub -V -N example_lncRNA.L16 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.L16.out -l nodes=1:ppn=8 -q batch <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/01runRNAseq_example_lncRNA_L16.sh' `
      job_ids="${job_ids}afterok:${current_job_id},"
      current_job_id=`qsub -V -N example_lncRNA.L21 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.L21.out -l nodes=1:ppn=8 -q batch <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/01runRNAseq_example_lncRNA_L21.sh' `
      job_ids="${job_ids}afterok:${current_job_id},"
      current_job_id=`qsub -V -N example_lncRNA.L22 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.L22.out -l nodes=1:ppn=8 -q batch <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/01runRNAseq_example_lncRNA_L22.sh' `
      job_ids="${job_ids}afterok:${current_job_id},"
      current_job_id=`qsub -V -N example_lncRNA.L23 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.L23.out -l nodes=1:ppn=8 -q batch <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/01runRNAseq_example_lncRNA_L23.sh' `
      job_ids="${job_ids}afterok:${current_job_id},"
      current_job_id=`qsub -V -N example_lncRNA.L24 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.L24.out -l nodes=1:ppn=8 -q batch <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/01runRNAseq_example_lncRNA_L24.sh' `
      job_ids="${job_ids}afterok:${current_job_id},"
     nohup bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/02runDiff_KEGG_UP_DOWN.sh &
     job_ids=${job_ids%?}
     current_job_id=`qsub -V -N example_lncRNA.diffgene -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.diffgene.out -l nodes=1:ppn=1 -q batch  -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/02runDiff_example_lncRNA.sh' `
     job_ids2="${job_ids2}afterok:${current_job_id},"
     current_job_id=`qsub -V -N example_lncRNA.final -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.final.out -l nodes=1:ppn=8 -q batch  -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/03runfinal_example_lncRNA.sh' `
     job_ids2="${job_ids2}afterok:${current_job_id},"
     job_ids2=${job_ids2%?}
     qsub -V -N example_lncRNA.report -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.report.out -l nodes=1:ppn=1 -q batch  -W depend=$job_ids2 <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/get_mRNA_report.sh'
      current_job_id=` qsub -V -N example_lncRNA.new.gene -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.new.gene.out -l nodes=1:ppn=8 -q batch  -W depend=$job_ids2 <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/04runnew_gene.sh' `
      job_ids6="${job_ids6}afterok:${current_job_id},"
      current_job_id=` qsub -V -N example_lncRNA.AS -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.AS.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids2 <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/06runAS.sh' `
      job_ids6="${job_ids6}afterok:${current_job_id},"
     job_ids6=${job_ids6%?}
     qsub -V -N example_lncRNA.mRNA_advanced_report -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.mRNA_advanced_report.out -l nodes=1:ppn=8 -q batch  -W depend=$job_ids6 <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/get_mRNA_advanced_report.sh'
      current_job_id=`qsub -V -N example_lncRNA.lncRNA -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.lncRNA.out -l nodes=1:ppn=8 -q batch  -W depend=$job_ids2 <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/05runlncRNA_analysis.sh' `
      job_ids3="${job_ids3}afterok:${current_job_id},"
      job_ids3=${job_ids3%?}
      qsub -V -N example_lncRNA.lncRNA_report -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.lncRNA_report.out -l nodes=1:ppn=8 -q batch  -W depend=$job_ids3 <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/get_lncRNA_report.sh'      
      qsub -V -N example_lncRNA.lncRNA_coexp -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/example_lncRNA.lncRNA_coexp.out -l nodes=1:ppn=8 -q batch  -W depend=$job_ids3 <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/06runlncRNA_co_exp_target_miRNA.sh' 
      current_job_id=`qsub -V -N circRNA.L13 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.L13.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/09run_circRNA_example_lncRNA_L13.sh' `
      job_ids4="${job_ids4}afterok:${current_job_id},"
      current_job_id=`qsub -V -N circRNA.L15 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.L15.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/09run_circRNA_example_lncRNA_L15.sh' `
      job_ids4="${job_ids4}afterok:${current_job_id},"
      current_job_id=`qsub -V -N circRNA.L17 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.L17.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/09run_circRNA_example_lncRNA_L17.sh' `
      job_ids4="${job_ids4}afterok:${current_job_id},"
      current_job_id=`qsub -V -N circRNA.L19 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.L19.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/09run_circRNA_example_lncRNA_L19.sh' `
      job_ids4="${job_ids4}afterok:${current_job_id},"
      current_job_id=`qsub -V -N circRNA.L16 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.L16.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/09run_circRNA_example_lncRNA_L16.sh' `
      job_ids4="${job_ids4}afterok:${current_job_id},"
      current_job_id=`qsub -V -N circRNA.L21 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.L21.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/09run_circRNA_example_lncRNA_L21.sh' `
      job_ids4="${job_ids4}afterok:${current_job_id},"
      current_job_id=`qsub -V -N circRNA.L22 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.L22.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/09run_circRNA_example_lncRNA_L22.sh' `
      job_ids4="${job_ids4}afterok:${current_job_id},"
      current_job_id=`qsub -V -N circRNA.L23 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.L23.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/09run_circRNA_example_lncRNA_L23.sh' `
      job_ids4="${job_ids4}afterok:${current_job_id},"
      current_job_id=`qsub -V -N circRNA.L24 -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.L24.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/09run_circRNA_example_lncRNA_L24.sh' `
      job_ids4="${job_ids4}afterok:${current_job_id},"
      job_ids4=${job_ids4%?}
      current_job_id=`qsub -V -N circRNA.diff -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.diff.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids4 <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/10run_circRNA_diff.sh' `
      job_ids5="${job_ids5}afterok:${current_job_id},"
      job_ids5=${job_ids5%?}
      qsub -V -N circRNA.diff -j oe -o /data/CustomerData/rna/lixy/example_lncRNA/out/log/circRNA.report.out -l nodes=1:ppn=8 -q batch -W depend=$job_ids5 <<<'bash /data/CustomerData/rna/lixy/example_lncRNA/out/code/get_circRNA_report.sh'
