# AWS
#python pkb.py \
#  --cloud=AWS \
#  --machine_type=m5n.large \
#  --benchmarks=iperf,fio,coremark,ping,unixbench \
#  --iperf_runtime_in_seconds=30 \
#  --fio_jobfile=./config/AWS/fio.txt \
#  --zones=us-east-1a \
#  --csv_path output/aws/m5n_all_us.csv

# GCP
# python pkb.py \
#     --cloud=GCP \
#     --machine_type="{cpus: 1, memory: 1GiB}" \
#     --image_project=ubuntu-os-cloud \
#     --image=ubuntu-1604-xenial-v20210211 \
#     --benchmarks=iperf,fio,coremark,ping,unixbench \
#     --iperf_runtime_in_seconds=30 \
#     --fio_jobfile=./config/GCP/fio.txt \
#     --zone=europe-west3-a \
#     --zone=asia-southeast1-a \
#     --csv_path output/gcp/1cpu_1GiB_all_eu.csv

# Azure
python pkb.py \
    --cloud=Azure \
    --machine_type=Standard_L8s_v2 \
    --benchmarks=iperf,fio,coremark,ping,unixbench \
    --iperf_runtime_in_seconds=30 \
    --fio_jobfile=./config/azure/fio.txt \
    --zones=eastus2 \
    --csv_path output/azure/Standard_L8s_v2_all_us2.csv

# Rackspace
# python pkb.py \
#     --cloud=Rackspace \
#     --machine_type=General1-1 \
#     --benchmarks=iperf,fio,coremark,ping,unixbench \
#     --iperf_runtime_in_seconds=30 \
#     --fio_jobfile=./config/rackspace/fio.txt \
#     --zone=FRA1 \
#     --csv_path output/rackspace/General1-1_all_eu.csv
# --zone=germanywestcentral-1

# AliCloud
#python pkb.py \
#    --cloud=AliCloud \
#    --machine_type=ecs.r6.4xlarge \
#    --benchmarks=iperf,fio,coremark,ping,unixbench \
#    --iperf_runtime_in_seconds=30 \
#    --fio_jobfile=./config/alicloud/fio.txt \
#    --zone=us-east-1a \
#    --data_disk_type=remote_ssd \
#    --csv_path output/alicloud/ecs.r6.4xlarge_all_us.csv
