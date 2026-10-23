import {
  Template,
  ExperimentRecord,
  ExecutionConfig,
  ProviderInfo
} from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/v1';

export class ApiError extends Error {
  constructor(
    public status: number,
    public title: string,
    public detail: string,
    public type: string = 'about:blank'
  ) {
    super(detail);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = 'Unknown API error occurred.';
    let title = 'Request Failed';
    let type = 'about:blank';
    try {
      const errJson = await res.json();
      if (errJson.detail) {
        if (typeof errJson.detail === 'object') {
          title = errJson.detail.title || title;
          errorDetail = errJson.detail.detail || JSON.stringify(errJson.detail);
          type = errJson.detail.type || type;
        } else {
          errorDetail = errJson.detail;
        }
      }
    } catch {
      errorDetail = await res.text();
    }
    throw new ApiError(res.status, title, errorDetail, type);
  }
  return res.json();
}

export const api = {
  async getTemplates(): Promise<Template[]> {
    const res = await fetch(`${API_BASE}/templates`);
    return handleResponse<Template[]>(res);
  },

  async createExperiment(payload: { prompt_text?: string; template_id?: string }): Promise<ExperimentRecord> {
    const res = await fetch(`${API_BASE}/experiments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return handleResponse<ExperimentRecord>(res);
  },

  async getExperiment(id: string): Promise<ExperimentRecord> {
    const res = await fetch(`${API_BASE}/experiments/${id}`);
    return handleResponse<ExperimentRecord>(res);
  },

  async listExperiments(): Promise<ExperimentRecord[]> {
    const res = await fetch(`${API_BASE}/experiments`);
    return handleResponse<ExperimentRecord[]>(res);
  },

  async regenerateCode(id: string, promptText?: string): Promise<ExperimentRecord> {
    const res = await fetch(`${API_BASE}/experiments/${id}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt_text: promptText })
    });
    return handleResponse<ExperimentRecord>(res);
  },

  async validateCode(id: string, code: string): Promise<ExperimentRecord> {
    const res = await fetch(`${API_BASE}/experiments/${id}/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });
    return handleResponse<ExperimentRecord>(res);
  },

  async executeExperiment(
    id: string,
    config: ExecutionConfig,
    hardwareToken?: string
  ): Promise<ExperimentRecord> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Idempotency-Key': `exp-exec-${id}-${Date.now()}`
    };

    const res = await fetch(`${API_BASE}/experiments/${id}/execute`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        execution_config: config,
        hardware_confirmation_token: hardwareToken
      })
    });
    return handleResponse<ExperimentRecord>(res);
  },

  async updateSharing(
    id: string,
    sharing: { repository?: boolean; dataset?: boolean; social?: boolean; research_package?: boolean }
  ): Promise<ExperimentRecord> {
    const res = await fetch(`${API_BASE}/experiments/${id}/sharing`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(sharing)
    });
    return handleResponse<ExperimentRecord>(res);
  },

  async getColabUrl(id: string): Promise<{ colab_url: string }> {
    const res = await fetch(`${API_BASE}/experiments/${id}/export/colab`);
    return handleResponse<{ colab_url: string }>(res);
  },

  async getProviders(): Promise<ProviderInfo[]> {
    const res = await fetch(`${API_BASE}/providers`);
    return handleResponse<ProviderInfo[]>(res);
  }
};
