import tarfile, os

CONDA_TAR_LOC = "D:\\home\site\\wwwroot\\conda"
CONDRUNTIME = os.path.join(CONDA_TAR_LOC, "condaruntime.tar.gz")

condatar = tarfile.open(name=CONDARUNTIME, mode="r:gz")
condatar.extractAll(CONDA_TAR_LOC)

os.remove(CONDARUNTIME)
