from create_security_group import create_sg
from create_launch_template import create_template
from create_asg import create_asg

def deploy_backend():
    sg_id = create_sg()
    lt_id = create_template(sg_id)
    create_asg(lt_id)

if __name__ == "__main__":
    deploy_backend()