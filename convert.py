import yaml

def load_github_workflow(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def save_gitlab_ci(data, file_path):
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

def convert_github_to_gitlab(github_workflow):
    gitlab_ci = {}

    # Map GitHub jobs to GitLab stages
    gitlab_ci['stages'] = list(github_workflow.get('jobs', {}).keys())

    # Convert jobs
    for job_name, job_data in github_workflow.get('jobs', {}).items():
        gitlab_ci[job_name] = {
            'stage': job_name,
            'script': job_data.get('steps', []),
        }

        # Map "runs-on" to "tags" in GitLab (adjust as needed)
        runs_on = job_data.get('runs-on')
        if runs_on:
            gitlab_ci[job_name]['tags'] = [runs_on]

        # Map GitHub steps to GitLab script
        scripts = []
        for step in job_data.get('steps', []):
            if 'run' in step:
                scripts.append(step['run'])
        gitlab_ci[job_name]['script'] = scripts

    return gitlab_ci

def main():
    github_file_path = '.github/workflows/main.yml'
    gitlab_file_path = '.gitlab-ci.yml'

    # Load GitHub Actions workflow
    github_workflow = load_github_workflow(github_file_path)

    # Convert to GitLab CI configuration
    gitlab_ci = convert_github_to_gitlab(github_workflow)

    # Save as .gitlab-ci.yml
    save_gitlab_ci(gitlab_ci, gitlab_file_path)
    print(f"Converted {github_file_path} to {gitlab_file_path}")

if __name__ == "__main__":
    main()
